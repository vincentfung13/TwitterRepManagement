import json
import nltk
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import *
import unicodedata

# Read the traning set and intellectually classified results
all_tweets = open("/Users/vincentfung13/Development/Level 4/Project/Tweets/pre.3ent.json", 'r')
classification_results = open("/Users/vincentfung13/Development/Level 4/Project/Tweets/pre.3ent.gold", 'r')

# Hard-coded method to retrive tweet category and entity related from the given traning set
def getAtrribute(tweet, key):
    tweet_json = json.loads(tweet)
    id = tweet_json.get('id')
    if key == 'category':
        for line in classification_results:
            if str(id) in line:
                return line[38:len(line) - 2]
    elif key == 'entity':
        for line in classification_results:
            if str(id) in line:
                return line[1:14]

# Construct a list of dictionary to hold text and catagory of tweets
def containsPunctuation(word):
    for symbol in string.punctuation:
        if symbol in word: return True
    return False

def processTweetText(tweet):
    stopset = list(set(stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    tweet_text = json.loads(tweet)['text'].encode('ascii', 'ignore').lower()
    tweet_text = word_tokenize(tweet_text)
#    tweet_text = [stemmer.stem(word) for word in tweet_text]
    tweet_text = [word for word in tweet_text if not containsPunctuation(word) and word not in stopset and word != '\n']
    return tweet_text

def construct_dict(tweets):
    all_words = []
    for line in tweets:
        all_words.extend(processTweetText(line))
    return nltk.FreqDist(all_words)

# Feature extractor for a single tweet - tweet is expected to be in json string
def tweet_feats(tweet):
    tweet_words = processTweetText(tweet)
    set_words = set(tweet_words)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in set_words)
    return features

all_words = construct_dict(all_tweets)
word_features = list(all_words)[10:]

all_tweets.close()

featureSets = []
all_tweets = open("/Users/vincentfung13/Development/Level 4/Project/Tweets/pre.3ent.json", 'r')
for tweet in all_tweets:
    category = getAtrribute(tweet, 'category')
    if category is None: continue
    featureSets.append((tweet_feats(tweet), category))
all_tweets.close()

training_set, test_set = featureSets[1024:], featureSets[:1024]

print('Training the classifier')
classifier = nltk.NaiveBayesClassifier.train(training_set)
#classifier = nltk.classify.DecisionTreeClassifier.train(training_set, entropy_cutoff=0, support_cutoff=0)

print('Classifying the testing set')
print('The accuracy of this experiment is: ' + str(nltk.classify.accuracy(classifier, test_set)))

