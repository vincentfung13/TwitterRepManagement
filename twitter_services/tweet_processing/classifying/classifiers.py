import json
import nltk.classify
import DjangoSetup
from sklearn import cross_validation
from sklearn.svm import LinearSVC
from twitter_services.models import TweetTrainingSet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


class DimensionClassifier:
    def __init__(self):
        # Build a dictionary
        training_tweets = [json.loads(obj['json_str']) for obj in TweetTrainingSet.objects.values('json_str')]
        dictionary = []
        for training_tweet in training_tweets:
            dictionary.extend(TweetNormalizer.get_tokens(training_tweet, json=True))

        # Build a feature set
        self.word_feature = [entry[0] for entry in list(nltk.FreqDist(dictionary).most_common(2000))][10:2000]
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
        pass

    # Return true if the tweet is spam and false otherwise
    def is_spam(self, tweet):
        pass


if __name__ == '__main__':
    # Trying to apply cross validation
    feature_sets = DimensionClassifier().feature_sets
    cv = cross_validation.KFold(len(feature_sets), n_folds=5, shuffle=False, random_state=None)

    for traincv, testcv in cv:
        classifier_cv = DimensionClassifier()
        classifier_cv.train(training_set=feature_sets[traincv[0]:traincv[len(traincv)-1]])

        print 'SVM accuracy:', nltk.classify.util.accuracy(classifier_cv.classifier,
                                                           feature_sets[testcv[0]:testcv[len(testcv)-1]])