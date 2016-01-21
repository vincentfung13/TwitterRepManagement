from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import *
import string


# Given a individual tweet, the function returns a list of tokens
def get_tokens(tweet, json=False, **kwargs):
    stop_words = list(set(stopwords.words('english')))

    # Get rid of username handles, replace repeated sequence then tokenize the tweet
    tweet_tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
    if not json:
        tweet_tokens = tweet_tokenizer.tokenize(tweet.lower())
    else:
        tweet_tokens = tweet_tokenizer.tokenize(tweet['text'].encode('ascii', 'ignore').lower())
    tweet_words = [word for word in tweet_tokens
                   if not __contains_punctuation__(word) and word not in stop_words and word != '\n']

    # Apply stemming and remove duplicates words
    if kwargs.get('stemming', False):
        stemmer = SnowballStemmer('english')
        tweet_words = list(set([stemmer.stem(word) for word in tweet_words]))

    tweet_words = list(set(tweet_words))
    return tweet_words


def __contains_punctuation__(word):
    for symbol in string.punctuation:
        if symbol in word: return True
    return False
