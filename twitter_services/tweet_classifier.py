import os
import json
import nltk
import sys
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import *


# Returns the feature set of the given tweet, tweet should be a json string
def extract_feature(tweet):
    tweet_words = __process_text(tweet)
    features = {}
    for word in dictionary:
        features['contains({})'.format(word)] = (word in tweet_words)
    return features


# The argument tweet should be a json string
def __process_text(tweet):
    stopset = list(set(stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    tweet_tokens = word_tokenize(json.loads(tweet)['text'].encode('ascii', 'ignore').lower())
    tweet_words = [word for word in tweet_tokens
                   if not __contains_punctuation(word) and word not in stopset and word != '\n']
    # Appliy stemming and remove duplicates words
    tweet_words = list(set([stemmer.stem(word) for word in tweet_words]))
    return tweet_words


def __contains_punctuation(word):
    for symbol in string.punctuation:
        if symbol in word: return True
    return False


# Hard-coded
def get_dimension(tweet, classification_result):
    tweet_id = json.loads(tweet)['id_str']
    for line in classification_result:
        if line[17:35] == tweet_id and line[38:len(line) - 2] is not None:
            return line[38:len(line) - 2]
        else:
            return 'Undefined'


# Construct a dictionary at initialization
with open(os.getcwd() + '/Tweets/pre.3ent.json', 'r') as json_file:
    all_tweets = [line for line in json_file]

dictionary = []
for tweet in all_tweets:
    dictionary.extend(__process_text(tweet))
dictionary = list(nltk.FreqDist(dictionary))[200:]

with open(sys.path[0] + '/Tweets/pre.3ent.gold', 'r') as classification_results:
    feature_sets = [(extract_feature(tweet), get_dimension(tweet, classification_results)) for tweet in all_tweets]

training_set, test_set = feature_sets[1024:], feature_sets[:1024]

print 'Training the classifier'
classifier = nltk.NaiveBayesClassifier.train(training_set)
# classifier = nltk.classify.DecisionTreeClassifier.train(training_set, entropy_cutoff=0, support_cutoff=0)

print 'Classifying the testing set'
print 'The accuracy of this experiment is: ' + str(nltk.classify.accuracy(classifier, test_set))
