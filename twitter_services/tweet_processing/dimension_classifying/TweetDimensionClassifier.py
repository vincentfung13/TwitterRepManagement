import json

import nltk.classify
from sklearn import cross_validation
from sklearn.svm import LinearSVC

if __name__ == '__main__':
    import DjangoSetup
from twitter_services.models import TweetTrainingSet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


# Returns the feature set of the given tweet, tweet should be a json string
def __extract_feature(tweet):
    tweet_words = TweetNormalizer.normalize_tweet(tweet)
    features = {}
    for word in word_feature:
        features['contains({})'.format(word)] = (word in tweet_words)
    return features


def classify(tweet):
    return classifier.classify(__extract_feature(tweet))

# Construct a dictionary at the beginning
# TODO: Data model needs to be modified for different approach to obtain tweet list
all_tweets = [json.loads(obj['json_str']) for obj in TweetTrainingSet.objects.values('json_str')]
dictionary = []
for tweet in all_tweets:
    dictionary.extend(TweetNormalizer.normalize_tweet(tweet))
dictionary = list(nltk.FreqDist(dictionary).most_common(2000))
word_feature = [entry[0] for entry in dictionary]


# Fetched the intellectual classification results and build the feature sets
feature_sets = [(__extract_feature(tweet), tweet.get('reputation_dimension'))
                for tweet in all_tweets if tweet.get('reputation_dimension') is not None]
training_set = feature_sets


# Training and testing the classifier
classifier = nltk.classify.SklearnClassifier(LinearSVC())
print 'DIMENSION CLASSIFIER: Training the classifier'
classifier.train(training_set)

if __name__ == '__main__':
    # Trying to apply cross validation
    cv = cross_validation.KFold(len(feature_sets), n_folds=5, shuffle=False, random_state=None)

    for traincv, testcv in cv:
        classifier_cv = nltk.classify.SklearnClassifier(LinearSVC())\
            .train(feature_sets[traincv[0]:traincv[len(traincv)-1]])
        print 'SVM accuracy:', nltk.classify.util.accuracy(classifier_cv, feature_sets[testcv[0]:testcv[len(testcv)-1]])