import tweepy

consumer_key = 'xBUcDmrEVJPxNgQ2UHCak9WuX'
consumer_secret = 'l5ZrwQruD3Sw1rAgz61GJQlyC9C1oB7PwZ2MYQmYanirnd3mnK'
access_token = '601685838-o5fHz8JIMwwz4GHjLUDrsHjzlKpAGyncldDm10Db'
access_token_secret = 'NafhBNpc1k80qw4k0GXcceEwk6ja99RRK4uGesKNaTQeS'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Create a stream listener
class MyListener(tweepy.StreamListener):
    def on_data(self, status):
            # TODO: Classify tweet and insert relevant information in to the database
            pass

myStreamListener = MyListener()
myStream = tweepy.Stream(auth, myStreamListener)
myStream.filter(languages = ['en'], track=['Amazon', 'Apple', 'Tesco', 'BMW', 'Heineken', 'RBS'], async=True)