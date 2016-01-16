import json

import nltk.classify
from sklearn import cross_validation
from sklearn.svm import LinearSVC
import DjangoSetup
from twitter_services.models import TweetTrainingSet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


class DimensionClassifier:
    def __init__(self):
        # Build a dictionary
        training_tweets = [json.loads(obj['json_str']) for obj in TweetTrainingSet.objects.values('json_str')]
        dictionary = []
        for training_tweet in training_tweets:
            dictionary.extend(TweetNormalizer.normalize_tweet(training_tweet))

        # Build a feature set
        self.word_feature = [entry[0] for entry in list(nltk.FreqDist(dictionary).most_common(2000))]
        self.feature_sets = [(self.__extract_feature(tweet), tweet.get('reputation_dimension'))
                             for tweet in training_tweets if tweet.get('reputation_dimension') is not None]

        # Initialize and train a classifier
        self.classifier = nltk.classify.SklearnClassifier(LinearSVC())
        self.trained = False

    def train(self, **kwargs):
        # Train the classifier with all tweets in the training set
        print 'INFO: Training the classifier.'
        if kwargs['training_set'] is None:
            self.classifier.train(self.feature_sets)
        else:
            self.classifier.train(kwargs['training_set'])
        self.trained = True

    def classify(self, document):
        if not self.trained:
            print 'You haven''t provided a training set, training with the default training set'
            self.train()
        return self.classifier.classify(self.__extract_feature(document))

    def __extract_feature(self, tweet):
        tweet_words = TweetNormalizer.normalize_tweet(tweet)
        features = {}
        for word in self.word_feature:
            features['contains({})'.format(word)] = (word in tweet_words)
        return features

if __name__ == '__main__':
    # Trying to apply cross validation
    feature_sets = DimensionClassifier().feature_sets
    cv = cross_validation.KFold(len(feature_sets), n_folds=5, shuffle=False, random_state=None)

    for traincv, testcv in cv:
        classifier_cv = DimensionClassifier()
        classifier_cv.train(training_set=feature_sets[traincv[0]:traincv[len(traincv)-1]])

        print 'SVM accuracy:', nltk.classify.util.accuracy(classifier_cv.classifier,
                                                           feature_sets[testcv[0]:testcv[len(testcv)-1]])