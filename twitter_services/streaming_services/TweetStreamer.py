import DjangoSetup
import TweetProcessWorker
import multiprocessing
import tweepy
import json
from twitter_services.tweet_processing import utility
from twitter_services.tweet_processing.classifying.classifiers import DimensionClassifier, SpamDetector


# Create a stream listener
class MyListener(tweepy.StreamListener):
    def __init__(self, tweet_queue):
        super(tweepy.StreamListener, self).__init__()
        self.tweet_queue = tweet_queue

    def on_data(self, status):
        self.tweet_queue.put(json.loads(status))

    def on_error(self, status_code):
        print 'ERROR: the amount of tweets buffered has reached the buffer limit.'


if __name__ == '__main__':
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

