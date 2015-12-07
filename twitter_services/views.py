from django.shortcuts import render
from .models import Tweet
import json

entities_list = ['Apple', 'Amazon', 'Tesco', 'BMW', 'Heineken', 'HSBC']

dimension_list = ['Innovation', 'Governance', 'Leadership', 'Performance',
                  'Citizenship', 'Products & Services', 'Workplace', 'Undefined']


def __build_dict(tweet_orm):
    tweet_json = json.loads(tweet_orm.json_str)
    tweet_json['reputation_dimension'] = tweet_orm.reputation_dimension
    tweet_json['entity'] = tweet_orm.related_entity
    tweet_json['sentiment_score'] = tweet_orm.sentiment_score
    return tweet_json


# Create your views here.
def main(request):
    tweets_json = []
    for tweet in Tweet.objects.all().order_by('created_at'):
        tweets_json.append(json.dumps(__build_dict(tweet)))
    context = {'tweets': tweets_json,
               'entities_list': entities_list,
               }
    return render(request, 'twitter_services/main.html', context)


def tweets_filter(request, entity, dimension=None):
    tweets_filtered = []

    if dimension is not None:
        tweets = Tweet.objects.filter(related_entity=entity, reputation_dimension=dimension).order_by('created_at')
    else:
        tweets = Tweet.objects.filter(related_entity=entity).order_by('created_at')

    for tweet in tweets:
        tweets_filtered.append(json.dumps(__build_dict(tweet)))

    context = {'tweets': tweets_filtered,
               'entity': entity,
               'entities_list': entities_list,
               'dimension_list': dimension_list,
               'Dimension': dimension
               }
    return render(request, 'twitter_services/tweets_filter.html', context)
