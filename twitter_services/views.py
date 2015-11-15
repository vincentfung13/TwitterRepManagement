from django.shortcuts import render
from .models import Tweet
import json

entities_list = ['Apple', 'Amazon', 'Tesco', 'BMW', 'Heineken', 'HSBC']

dimension_list = ['Innovation', 'Governance', 'Leadership', 'Performance',
                  'Citizenship', 'Products & Services', 'Workplace', 'Undefined']


# Create your views here.
def main(request):
    tweets_json = []
    for tweet in Tweet.objects.all():
        tweets_json.append(json.dumps(json.loads(tweet.tweet_json)))
    context = {'tweets': tweets_json,
               'entities_list': entities_list,
               }
    return render(request, 'twitter_services/main.html', context)


def tweets_filter(request, entity, dimension=None):
    tweets_filtered = []

    for tweet in Tweet.objects.all():
        tweet_json = json.loads(tweet.tweet_json)
        if tweet_json['entity'] == entity:
            tweets_filtered.append(json.dumps(tweet_json))

    if dimension is not None:
        tweets_filtered = [tweet for tweet in tweets_filtered
                           if json.loads(tweet)['reputation_dimension'] == dimension]

    context = {'tweets': tweets_filtered,
               'entity': entity,
               'entities_list': entities_list,
               'dimension_list': dimension_list,
               'Dimension': dimension
               }
    return render(request, 'twitter_services/tweets_filter.html', context)
