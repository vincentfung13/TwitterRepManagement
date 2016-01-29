import datetime
import json
import pytz
from twitter_services.tweet_processing.sentiment_evaluating import TweetSentimentEvaluator

entities_list = ['Apple', 'Amazon', 'Tesco', 'BMW', 'Heineken', 'HSBC']

dimension_list = ['Innovation', 'Governance', 'Leadership', 'Performance',
                  'Citizenship', 'Products & Services', 'Workplace', 'Undefined']

dict_keyword_entity = dict()
dict_keyword_entity['Apple'] = ['iphone', 'ipad', 'macbook', 'mac', 'ipod', ]
dict_keyword_entity['Amazon'] = ['amazon', ]
dict_keyword_entity['Tesco'] = ['tesco', ]
dict_keyword_entity['BMW'] = ['bmw', ]
dict_keyword_entity['Heineken'] = ['heineken', ]
dict_keyword_entity['HSBC'] = ['hsbc', ]


def fetch_entity(tweet_json):
    text_lower = tweet_json['text'].lower()
    for entity, dictionary in dict_keyword_entity.iteritems():
        for word in dictionary:
            if word.lower() in text_lower:
                return entity


def convert_to_datetime(timestamp_ms):
    # Slicing of the last three digits because python expects timestamp to be in second
    timestamp = str(timestamp_ms)[0:-3]
    return datetime.datetime.fromtimestamp(int(timestamp))


# Build a dictionary of tweets to put into views from an ORM object
def build_dict(tweet_orm):
    tweet_json = json.loads(tweet_orm.json_str)
    tweet_json['reputation_dimension'] = tweet_orm.reputation_dimension
    tweet_json['entity'] = tweet_orm.related_entity
    tweet_json['sentiment_score'] = tweet_orm.sentiment_score
    return tweet_json


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


# Function to determine if a score represents negative sentiment
def is_negative(senti_score):
    negative = int(senti_score[len(senti_score) - 1])
    if negative >= 2:
        return True
    else:
        return False

