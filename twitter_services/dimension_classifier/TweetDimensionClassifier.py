import os
import json
import nltk
import sys
import string
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import *

import nltk.classify
from sklearn.svm import LinearSVC

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


# Construct a dictionary at initialization
with open(os.getcwd() + '/resources/Tweets/pre.3ent.json', 'r') as json_file:
    all_tweets = [line for line in json_file]

dictionary = []
for tweet in all_tweets:
    dictionary.extend(__process_text(tweet))
dictionary = list(nltk.FreqDist(dictionary).most_common(2000))
word_feature = [entry[0] for entry in dictionary]

with open(sys.path[0] + '/resources/Tweets/pre.3ent.gold', 'r+') as classification_results:
    dimension_dict = {}
    for entry in classification_results:
        dimension_dict[entry[17:35]] = entry[38:len(line) - 2]

feature_sets = [(extract_feature(tweet), dimension_dict[json.loads(tweet).get('id_str')]) for tweet in all_tweets
                if dimension_dict[json.loads(tweet).get('id_str')] is not None]

training_set, test_set = feature_sets[1024:], feature_sets[:1024]

print 'Training the classifier'
# classifier = nltk.NaiveBayesClassifier.train(training_set)
# classifier = nltk.classify.DecisionTreeClassifier.train(training_set, entropy_cutoff=0, support_cutoff=0)
classifier = nltk.classify.SklearnClassifier(LinearSVC())
classifier.train(training_set)

# with open(sys.path[0] + '/resources/Tweets/pre.3ent.gold', 'r') as classification_results:
#     for item in all_tweets[1024:]:
#         dimension = dimension_dict[json.loads(item).get('id_str')]
#         # if dimension is not None:
#         print dimension
#
#     for item in all_tweets[1025: len(all_tweets) - 1]:
#         dimension = dimension_dict[json.loads(item).get('id_str')]
#         classified = classifier.classify(extract_feature(item))
#         if dimension is not None:
#             print dimension, classified

print 'Classifying the testing set'
print 'The accuracy of this experiment is: ' + str(nltk.classify.accuracy(classifier, test_set))
