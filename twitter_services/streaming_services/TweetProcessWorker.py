import json
import multiprocessing

from twitter_services.models import Tweet
from twitter_services.tweet_processing import utility
from twitter_services.tweet_processing.dimension_classifying import TweetDimensionClassifier
from twitter_services.tweet_processing.sentiment_evaluating import TweetSentimentEvaluator


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
    tweet_dict = {}
    tweet_json = json.loads(status)
    id_str = tweet_json['id_str']

    if is_reputation_affecting(tweet_json):
        reputation_dimension = TweetDimensionClassifier.classify(tweet_json)
        cluster = None
        related_entity = utility.fetch_entity(tweet_json)
        sentiment_score = TweetSentimentEvaluator.rate_sentiment(tweet_json)
        created_at = utility.convert_to_datetime(tweet_json['timestamp_ms'])

        tweet_dict['tweet_json'] = status
        tweet_dict['reputation_dimension'] = reputation_dimension
        tweet_dict['sentiment_score'] = sentiment_score
        tweet_dict['cluster'] = cluster
        tweet_dict['entity'] = related_entity
        tweet_dict['created_at'] = created_at

        # Insert the tweet into the databse if it is reputation-affecting

        try:
            Tweet.objects.create(tweet_id=id_str, json_str=tweet_dict['tweet_json'],
                                reputation_dimension=tweet_dict['reputation_dimension'],
                                related_entity=tweet_dict['entity'], sentiment_score=tweet_dict['sentiment_score'],
                                created_at=tweet_dict['created_at']).save()
            print 'Inserted tweet id: %s' % id_str

        except Exception:
            print 'STREAMING ERROR: IntegrityError %s for tweet: %s' \
                  % (Exception.message, tweet_json['text'])


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
