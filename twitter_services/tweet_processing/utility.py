import datetime,json


def convert_to_datetime(timestamp_ms):
    # Slicing of the last three digits because python expects timestamp to be in second
    timestamp = str(timestamp_ms)[0:-3]
    return datetime.datetime.fromtimestamp(int(timestamp))


dict_keyword_entity = dict()
dict_keyword_entity['Apple'] = ['iPhone', 'iPad', 'MacBook', 'Mac', 'iPod', ]
dict_keyword_entity['Amazon'] = ['Amazon', ]
dict_keyword_entity['Tesco'] = ['Tesco', ]
dict_keyword_entity['BMW'] = ['BMW', ]
dict_keyword_entity['Heineken'] = ['Heineken', ]
dict_keyword_entity['HSBC'] = ['HSBC', ]


def fetch_entity(tweet_json):
   # TODO: better to do some topic modelling to fetch entity
    text_lower = tweet_json['text'].lower()
    for entity, dictionary in dict_keyword_entity.iteritems():
        for word in dictionary:
            if word.lower() in text_lower:
                return entity
