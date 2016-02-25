import datetime
import json
import pytz
from user_handle.models import UserEntity
from django.contrib.auth.models import User
from twitter_services.geocoding.geocoders import LocalGeocoder
from twitter_services.tweet_processing.sentiment_evaluating import TweetSentimentEvaluator

entities_list = ['Apple', 'Amazon', 'Tesco', 'BMW', 'Heineken', 'HSBC']

dimension_list = ['Innovation', 'Governance', 'Leadership', 'Performance',
                  'Citizenship', 'Products & Services', 'Workplace', 'Undefined']

dict_keyword_entity = dict()
dict_keyword_entity['Apple'] = ['iphone', 'ipad', 'macbook', 'imac', 'ipod', ]
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


def get_view_content(request, tweets_orms):
    tweets_filtered = [tweet_orm.tweet for tweet_orm in tweets_orms]
    geocoder = LocalGeocoder()
    coordinates = geocoder.geocode_many(tweets_filtered)
    latitudes = [coordinate[0] for coordinate in coordinates]
    longitudes = [coordinate[1] for coordinate in coordinates]

    user = User.objects.get(username=request.user.username)
    interest_list = [ue_orm.entity for ue_orm in UserEntity.objects.filter(user=user)]

    return {
        'tweets': tweets_filtered[:100],
        'latitudes': latitudes,
        'longitudes': longitudes,
        'interest_list': interest_list
    }


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
    if negative > 2:
        return True
    else:
        return False


# Get the negative value given a senti_score
def get_negative_score(senti_score_list):
    return [int(senti_score[len(senti_score) - 1]) for senti_score in senti_score_list]


# Get the positive value given a senti_score
def get_positive_score(senti_score_list):
    return [int(senti_score[0]) for senti_score in senti_score_list]

