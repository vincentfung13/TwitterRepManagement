# Configure django
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'
django.setup()

import tweepy
import json
# from twitter_services.models import Tweet, TweetEntityDimension
from twitter_services.sentiment_evaluator import TweetSentimentEvaluator
from twitter_services.dimension_classifier import TweetDimensionClassifier

# Auth for using twitter API
consumer_key = 'xBUcDmrEVJPxNgQ2UHCak9WuX'
consumer_secret = 'l5ZrwQruD3Sw1rAgz61GJQlyC9C1oB7PwZ2MYQmYanirnd3mnK'
access_token = '601685838-o5fHz8JIMwwz4GHjLUDrsHjzlKpAGyncldDm10Db'
access_token_secret = 'NafhBNpc1k80qw4k0GXcceEwk6ja99RRK4uGesKNaTQeS'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# Create a stream listener
class MyListener(tweepy.StreamListener):
    def on_data(self, status):
        tweet_json = json.loads(status)
        text = tweet_json['text']
        rep_dimension = TweetDimensionClassifier.classifier.classify(TweetDimensionClassifier.extract_feature(status))
        senti_score = TweetSentimentEvaluator.rate_sentiment(status)
        entity_related = fetch_entity(status)
        id_str = tweet_json['id_str']

        # Insert the tweet into the databse if it is reputation-affecting
        # if is_reputation_affecting(status):
        #     tweet_db = Tweet.objects.create(tweet_id=id_str, tweet_json=status, sentiment_score=senti_score)
        #     tweet_db.tweetentitydimension_set.create(id='%s : %s' % (id_str, entity_related), entity=entity_related,
        #                                             dimension=rep_dimension)

        print 'Tweet text: %s, Dimension: %s, Sentiment: %s' % (text, rep_dimension, senti_score)


myStreamListener = MyListener()
myStream = tweepy.Stream(auth, myStreamListener)
myStream.filter(languages = ['en'], track=['Amazon', 'Apple', 'Tesco', 'BMW', 'Heineken', 'RBS'], async=True)


# Retrieve entity from a tweet
def fetch_entity(tweet):
    pass


# Function to determine if a tweet is reputation-affecting
# @return True if it is and False otherwise
def is_reputation_affecting(tweet):
    pass