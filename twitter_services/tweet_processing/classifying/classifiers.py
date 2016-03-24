from TwitterRepManagement import settings
import nltk.classify
from sklearn import cross_validation
from sklearn.svm import LinearSVC

if __name__ == '__main__':
    import os
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'
    django.setup()

from twitter_services.models import TweetTrainingSet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


class DimensionClassifier:
    def __init__(self):
        # Build a dictionary
        training_tweets = [obj.tweet for obj in TweetTrainingSet.objects.all()]
        dictionary = []
        for training_tweet in training_tweets:
            dictionary.extend(TweetNormalizer.get_tokens(training_tweet, json=True))

        # Build a feature set
        self.word_feature = [entry[0] for entry in list(nltk.FreqDist(dictionary).most_common(2000))][100:2000]
        self.feature_sets = [(self.__extract_feature__(tweet), tweet.get('reputation_dimension'))
                             for tweet in training_tweets if tweet.get('reputation_dimension') is not None]

        # Initialize and train a classifier
        self.classifier = nltk.classify.SklearnClassifier(LinearSVC())
        self.trained = False

    def train(self, **kwargs):
        # Train the classifier with all tweets in the training set
        if not kwargs.has_key('training_set'):
            self.classifier.train(self.feature_sets)
        else:
            self.classifier.train(kwargs['training_set'])
        self.trained = True

    def classify(self, document):
        if not self.trained:
            self.train()
        return self.classifier.classify(self.__extract_feature__(document))

    def __extract_feature__(self, tweet):
        tweet_words = TweetNormalizer.get_tokens(tweet, json=True)
        features = {}
        for word in self.word_feature:
            features['contains({})'.format(word)] = (word in tweet_words)
        return features


# This classifier is used to identify spam tweets
class SpamDetector(object):
    def __init__(self):
        file_path = settings.BASE_DIR + '/twitter_services/tweet_processing/classifying/SpamCollection.txt'
        with open(file_path, 'r') as spam_collection:
            text_collections = []
            i = 0
            for line in spam_collection:
                if i > 2500:
                    break
                text = line.strip().split('\t')[1]
                category = line.strip().split('\t')[0]
                text_collections.append((TweetNormalizer.get_tokens(text), category))
                i += 1

        # build a word_feature dictionary of the data set
        all_words = []
        for text in text_collections:
            all_words.extend(text[0])
        self.word_feature = [entry[0] for entry in list(nltk.FreqDist(all_words).most_common(2000))]
        feature_sets = [(self.__extract_feature__(text[0], is_token=True), text[1])
                        for text in text_collections]

        # Initialize and train the classifier
        self.classifier = nltk.classify.SklearnClassifier(LinearSVC()).train(feature_sets)

    # Return true if the tweet is spam and false otherwise
    def is_spam(self, text):
        if self.classifier.classify(self.__extract_feature__(text)).lower() == 'spam':
            return True
        else:
            return False

    def __extract_feature__(self, data, is_token=False):
        if not is_token:
            tokens = TweetNormalizer.get_tokens(data, json=True)
        else:
            tokens = data
        features = {}
        for word in self.word_feature:
            features[u'contains({})'.format(word)] = (word in tokens)
        return features


if __name__ == '__main__':
    # Trying to apply cross validation
    feature_sets = DimensionClassifier().feature_sets
    cv = cross_validation.KFold(len(feature_sets), n_folds=100, shuffle=True, random_state=None)

    for traincv, testcv in cv:
        classifier_cv = DimensionClassifier()
        classifier_cv.train(training_set=feature_sets[traincv[0]:traincv[len(traincv)-1]])

        print 'SVM accuracy:', nltk.classify.util.accuracy(classifier_cv.classifier,
                                                           feature_sets[testcv[0]:testcv[len(testcv)-1]])