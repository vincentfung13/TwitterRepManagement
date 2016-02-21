import multiprocessing

from django.utils import timezone

from twitter_services.models import Tweet
from twitter_services.tweet_processing import utility
from twitter_services.tweet_processing.sentiment_evaluating import TweetSentimentEvaluator


class TweetProcessor(multiprocessing.Process):
    def __init__(self, tweet_queue, dimension_classifier, spam_detector):
        super(TweetProcessor, self).__init__()
        self.tweet_queue = tweet_queue
        self.dimension_classifier = dimension_classifier
        self.spam_detector = spam_detector
        # Buffer for bulk create
        self.tweets_buffer = []
        self.buffer_size = 100

    def run(self):
        while True:
            status = self.tweet_queue.get()
            if not self.spam_detector.is_spam(status) and utility.is_reputation_affecting(status):
                id_str = status['id_str']
                status['reputation_dimension'] = self.dimension_classifier.classify(status)
                status['related_entity'] = utility.fetch_entity(status)
                status['sentiment_score'] = TweetSentimentEvaluator.rate_sentiment(status)
                self.tweets_buffer.append(Tweet(tweet_id=id_str, tweet=status, created_at=timezone.now()))
                print 'Tweet %s added to buffer, buffer size %d' % id_str, len(self.tweets_buffer)

                if len(self.tweets_buffer) >= self.buffer_size:
                    Tweet.objects.bulk_create(self.tweets_buffer)
                    del self.tweets_buffer[:]
                    print 'INFO: Bulk created 100 tweets %s' % timezone.now()



