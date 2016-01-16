import datetime
import json


entities_list = ['Apple', 'Amazon', 'Tesco', 'BMW', 'Heineken', 'HSBC']

dimension_list = ['Innovation', 'Governance', 'Leadership', 'Performance',
                  'Citizenship', 'Products & Services', 'Workplace', 'Undefined']

dict_keyword_entity = dict()
dict_keyword_entity['Apple'] = ['iPhone', 'iPad', 'MacBook', 'Mac', 'iPod', ]
dict_keyword_entity['Amazon'] = ['Amazon', ]
dict_keyword_entity['Tesco'] = ['Tesco', ]
dict_keyword_entity['BMW'] = ['BMW', ]
dict_keyword_entity['Heineken'] = ['Heineken', ]
dict_keyword_entity['HSBC'] = ['HSBC', ]


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


def build_dict(tweet_orm):
    tweet_json = json.loads(tweet_orm.json_str)
    tweet_json['reputation_dimension'] = tweet_orm.reputation_dimension
    tweet_json['entity'] = tweet_orm.related_entity
    tweet_json['sentiment_score'] = tweet_orm.sentiment_score
    return tweet_json
