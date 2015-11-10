import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'
django.setup()

import json
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import *
import nltk.classify
from sklearn.svm import LinearSVC
from sklearn import cross_validation
from twitter_services.models import TweetTrainingSet, Tweet, TweetEntityDimension


# Returns the feature set of the given tweet, tweet should be a json string
def extract_feature(tweet):
    tweet_words = __process_text(tweet)
    features = {}
    for word in word_feature:
        features['contains({})'.format(word)] = (word in tweet_words)
    return features


# Given a individual tweet, the function returns a list of tokens
def __process_text(tweet):
    stop_words = list(set(stopwords.words('english')))

    # Get rid of username handles, replace repeated sequence then tokenize the tweet
    tweet_tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
    tweet_tokens = tweet_tokenizer.tokenize(json.loads(tweet)['text'].encode('ascii', 'ignore').lower())
    tweet_words = [word for word in tweet_tokens
                   if not __contains_punctuation(word) and word not in stop_words and word != '\n']

    # Appliy stemming and remove duplicates words
    stemmer = SnowballStemmer("english")
    tweet_words = list(set([stemmer.stem(word) for word in tweet_words]))

    return tweet_words


def __contains_punctuation(word):
    for symbol in string.punctuation:
        if symbol in word: return True
    return False

# Construct a dictionary at the beginning
all_tweets = [obj['tweet_json'] for obj in Tweet.objects.values('tweet_json')]

dictionary = []
for tweet in all_tweets:
    dictionary.extend(__process_text(tweet))
dictionary = list(nltk.FreqDist(dictionary).most_common(2000))
word_feature = [entry[0] for entry in dictionary]

# Fetched the intellectual classification results
dimension_dict = {}
for entry in TweetEntityDimension.objects.values('tweet_id', 'dimension'):
    dimension_dict[entry['tweet_id']] = entry['dimension']

# Build feature sets for training and testing
feature_sets = [(extract_feature(tweet), dimension_dict[json.loads(tweet).get('id_str')]) for tweet in all_tweets
                if dimension_dict[json.loads(tweet).get('id_str')] is not None]



training_set, test_set = feature_sets[202:], feature_sets[:1809]

# Training and testing the classifier
# classifier = nltk.NaiveBayesClassifier.train(training_set)
# classifier = nltk.classify.DecisionTreeClassifier.train(training_set, entropy_cutoff=0, support_cutoff=0)
# classifier = nltk.classify.SklearnClassifier(LinearSVC())
# print 'Training the classifier'
# classifier.train(training_set)

# hit_count = 0
# miss_count = 0
# for item in all_tweets[1025: len(all_tweets) - 1]:
#     dimension = dimension_dict[json.loads(item).get('id_str')]
#     classified = classifier.classify(extract_feature(item))
#     # if dimension is not None:
#     print dimension, classified

# print 'Classifying the testing set'
# print 'The accuracy of the experiment is: ' + str(nltk.classify.accuracy(classifier, test_set))

# Trying to apply cross validation
cv = cross_validation.KFold(len(feature_sets), n_folds=10, shuffle=False, random_state=None)

for traincv, testcv in cv:
    classifier_cv = nltk.classify.SklearnClassifier(LinearSVC()).train(feature_sets[traincv[0]:traincv[len(traincv)-1]])
    print 'accuracy:', nltk.classify.util.accuracy(classifier_cv, training_set[testcv[0]:testcv[len(testcv)-1]])
