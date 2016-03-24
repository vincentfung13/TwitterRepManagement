from django.core.management.base import NoArgsCommand
import multiprocessing
import tweepy
from twitter_services.tweet_processing import utility
from twitter_services.tweet_processing.classifying.classifiers import DimensionClassifier, SpamDetector
from twitter_services.streaming_services.TweetStreamer import MyListener
from twitter_services.streaming_services import TweetProcessWorker


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        apple_dic = utility.dict_keyword_entity['Apple']
        amazon_dic = utility.dict_keyword_entity['Amazon']
        tesco_dic = utility.dict_keyword_entity['Tesco']
        bmw_dic = utility.dict_keyword_entity['BMW']
        heineken_dic = utility.dict_keyword_entity['Heineken']
        hsbc_dic = utility.dict_keyword_entity['HSBC']
        track_list = apple_dic + amazon_dic + tesco_dic + bmw_dic + heineken_dic + hsbc_dic

        tweet_queue = multiprocessing.JoinableQueue()
        num_consumers = multiprocessing.cpu_count()

        dimension_classifier = DimensionClassifier()
        spam_detector = SpamDetector()
        tweet_processors = [TweetProcessWorker.TweetProcessor(tweet_queue, dimension_classifier, spam_detector)
                            for i in xrange(num_consumers)]

        for processor in tweet_processors:
            processor.start()

        # Auth for using twitter API
        consumer_key = 'xBUcDmrEVJPxNgQ2UHCak9WuX'
        consumer_secret = 'l5ZrwQruD3Sw1rAgz61GJQlyC9C1oB7PwZ2MYQmYanirnd3mnK'
        access_token = '601685838-o5fHz8JIMwwz4GHjLUDrsHjzlKpAGyncldDm10Db'
        access_token_secret = 'NafhBNpc1k80qw4k0GXcceEwk6ja99RRK4uGesKNaTQeS'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        myStreamListener = MyListener(tweet_queue)
        myStream = tweepy.Stream(auth, myStreamListener)
        myStream.filter(languages=['en'], track=track_list, async=True)
