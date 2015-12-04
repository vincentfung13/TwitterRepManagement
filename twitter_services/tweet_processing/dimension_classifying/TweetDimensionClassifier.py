import json

import nltk.classify
from sklearn import cross_validation
from sklearn.svm import LinearSVC

from twitter_services.models import TweetTrainingSet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


# Returns the feature set of the given tweet, tweet should be a json string
def extract_feature(tweet):
    tweet_words = TweetNormalizer.normalize_tweet(tweet)
    features = {}
    for word in word_feature:
        features['contains({})'.format(word)] = (word in tweet_words)
    return features


# Construct a dictionary at the beginning
all_tweets = [obj['tweet_json'] for obj in TweetTrainingSet.objects.values('tweet_json')]
dictionary = []
for tweet in all_tweets:
    dictionary.extend(TweetNormalizer.normalize_tweet(tweet))
print len(dictionary)
dictionary = list(nltk.FreqDist(dictionary).most_common(2000))
word_feature = [entry[0] for entry in dictionary]


# Fetched the intellectual classification results and build the feature sets
feature_sets = [(extract_feature(tweet), json.loads(tweet).get('reputation_dimension'))
                for tweet in all_tweets if json.loads(tweet).get('reputation_dimension') is not None]
training_set, test_set = feature_sets[202:], feature_sets[:1809]


# Training and testing the classifier
classifier = nltk.classify.SklearnClassifier(LinearSVC())
print 'Training the classifier'
classifier.train(training_set)

if __name__ == '__main__':
    # Trying to apply cross validation
    cv = cross_validation.KFold(len(feature_sets), n_folds=5, shuffle=False, random_state=None)

    for traincv, testcv in cv:
        classifier_cv = nltk.classify.SklearnClassifier(LinearSVC())\
            .train(feature_sets[traincv[0]:traincv[len(traincv)-1]])
        print 'SVM accuracy:', nltk.classify.util.accuracy(classifier_cv, feature_sets[testcv[0]:testcv[len(testcv)-1]])