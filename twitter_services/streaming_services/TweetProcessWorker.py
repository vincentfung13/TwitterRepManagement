# Configure django
# import os, django
# os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'
# django.setup()

import re, json, multiprocessing
from twitter_services.models import Tweet, TweetEntityDimension
from twitter_services.sentiment_evaluator import TweetSentimentEvaluator
from twitter_services.dimension_classifier import TweetDimensionClassifier


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
    text = tweet_json['text']
    rep_dimension = TweetDimensionClassifier.classifier.classify(TweetDimensionClassifier.extract_feature(status))
    senti_score = TweetSentimentEvaluator.rate_sentiment(status)
    entity_related = fetch_entity(status)
    id_str = tweet_json['id_str']
    affecting = is_reputation_affecting(status)
    # Insert the tweet into the databse if it is reputation-affecting
    if is_reputation_affecting(status):
        tweet_db = Tweet.objects.create(tweet_id=id_str, tweet_json=status, sentiment_score=senti_score)
        tweet_db.tweetentitydimension_set.create(id='%s : %s' % (id_str, entity_related), entity=entity_related,
                                                dimension=rep_dimension)
        tweet_db.save()

    print 'Tweet text: %s, Dimension: %s, Sentiment: %s, Entity: %s, Affecting: %s' % \
        (text, rep_dimension, senti_score, entity_related, affecting)


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
    if int(negative) > 2:
        return True
    else:
        return False