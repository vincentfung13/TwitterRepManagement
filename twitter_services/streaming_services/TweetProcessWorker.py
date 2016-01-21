import json
import multiprocessing

from twitter_services.models import Tweet
from twitter_services.tweet_processing import utility
from twitter_services.tweet_processing.sentiment_evaluating import TweetSentimentEvaluator


class TweetProcessor(multiprocessing.Process):
    def __init__(self, tweet_queue, dimension_classifier, spam_detector):
        super(TweetProcessor, self).__init__()
        self.tweet_queue = tweet_queue
        self.dimension_classifier = dimension_classifier
        self.spam_detector = spam_detector

    def run(self):
        while True:
            status = self.tweet_queue.get()
            process_tweet(status, self.dimension_classifier, self.spam_detector)


# Process a single tweet and insert it into the db if it fits the requirements
def process_tweet(status, dimension_classifier, spam_detector):
    tweet_dict = {}
    tweet_json = json.loads(status)
    id_str = tweet_json['id_str']

    if (not spam_detector.is_spam(tweet_json)) and utility.is_reputation_affecting(tweet_json):
        reputation_dimension = dimension_classifier.classify(tweet_json)
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

        # Insert the tweet into the database if it is reputation-affecting
        try:
            Tweet.objects.create(tweet_id=id_str, json_str=tweet_dict['tweet_json'],
                                reputation_dimension=tweet_dict['reputation_dimension'],
                                related_entity=tweet_dict['entity'], sentiment_score=tweet_dict['sentiment_score'],
                                created_at=tweet_dict['created_at']).save()
            print 'Inserted tweet id: %s' % id_str

        except Exception, IntegrityError:
            print 'STREAMING ERROR: IntegrityError %s for tweet: %s' \
                    % (IntegrityError.message, tweet_json['text'])
