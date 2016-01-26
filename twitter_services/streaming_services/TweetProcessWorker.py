import multiprocessing

from django.db import transaction, DatabaseError

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
def process_tweet(tweet_json, dimension_classifier, spam_detector):
    if (not spam_detector.is_spam(tweet_json)) and utility.is_reputation_affecting(tweet_json):
        id_str = tweet_json['id_str']
        tweet_json['reputation_dimension'] = dimension_classifier.classify(tweet_json)
        tweet_json['related_entity'] = utility.fetch_entity(tweet_json)
        tweet_json['sentiment_score'] = TweetSentimentEvaluator.rate_sentiment(tweet_json)

        # Insert the tweet into the database if it is reputation-affecting
        try:
            Tweet.objects.create(tweet_id=id_str, tweet=tweet_json).save()
            print 'Inserted tweet id: %s' % id_str

        except DatabaseError:
            print 'Database Error: Bad query! Rolling back transaction.'
            transaction.rollback()

