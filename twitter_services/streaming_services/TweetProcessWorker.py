import json
import multiprocessing

from twitter_services.models import Tweet
from twitter_services.tweet_processing.dimension_classifying import TweetDimensionClassifier
from twitter_services.tweet_processing.sentiment_evaluating import TweetSentimentEvaluator

dict_keyword_entity = dict()
dict_keyword_entity['Apple'] = ['iPhone', 'iPad', 'MacBook', 'Mac', 'iPod', ]
dict_keyword_entity['Amazon'] = ['Amazon', ]
dict_keyword_entity['Tesco'] = ['Tesco', ]
dict_keyword_entity['BMW'] = ['BMW', ]
dict_keyword_entity['Heineken'] = ['Heineken', ]
dict_keyword_entity['HSBC'] = ['HSBC', ]


class TweetProcessor(multiprocessing.Process):
    def __init__(self, tweet_queue):
        super(TweetProcessor, self).__init__()
        self.tweet_queue = tweet_queue

    def run(self):
        while True:
            status = self.tweet_queue.get()
            process_tweet(status)


# Process a single tweet and insert it into the db if it fits the requirements
def process_tweet(status):
    tweet_json = json.loads(status)
    tweet_json['reputation_dimension'] = \
        TweetDimensionClassifier.classifier.classify(TweetDimensionClassifier.extract_feature(status))
    tweet_json['sentiment_score'] = TweetSentimentEvaluator.rate_sentiment(status)
    tweet_json['entity'] = fetch_entity(status)
    id_str = tweet_json['id_str']

    # Insert the tweet into the databse if it is reputation-affecting
    if is_reputation_affecting(status):
        try:
            Tweet.objects.create(tweet_id=id_str, tweet_json=json.dumps(tweet_json)).save()
            print 'Inserted tweet id: %s' % id_str
        except:
            print 'Tweet %s already exists' % id_str


# Retrieve entity from a tweet
def fetch_entity(tweet):
    # TODO: better to do some topic modelling to fetch entity
    text_lower = json.loads(tweet)['text'].lower()
    for entity, dictionary in dict_keyword_entity.iteritems():
        for word in dictionary:
            if word.lower() in text_lower:
                return entity


# Function to determine if a tweet is reputation-affecting
# @return True if it is and False otherwise
def is_reputation_affecting(tweet):
    senti_score = TweetSentimentEvaluator.rate_sentiment(tweet)
    negative = senti_score[len(senti_score) - 1]
    positive = senti_score[0]
    if int(negative) >= 2 or int(positive) >= 2:
        return True
    else:
        return False
