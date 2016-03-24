import tweepy
import json

# Create a stream listener
class MyListener(tweepy.StreamListener):
    def __init__(self, tweet_queue):
        super(tweepy.StreamListener, self).__init__()
        self.tweet_queue = tweet_queue

    def on_data(self, status):
        self.tweet_queue.put(json.loads(status))

    def on_error(self, status_code):
        print 'ERROR: the amount of tweets buffered has reached the buffer limit.'

