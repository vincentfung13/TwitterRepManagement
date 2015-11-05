from django.shortcuts import render
from .models import Tweet, Tweet_Reputation_Dimension
import json


# Create your views here.
def main(request):
    tweets_list = Tweet.objects.all()
    tweets_json = []

    entities_set = Tweet_Reputation_Dimension.objects.all().values('entity').distinct()
    # TODO: find a way to do make the upper line return a list of values only, look at QuerySet API.
    entities_list = []
    for item in entities_set:
        entities_list.append(item['entity'])

    for tweet in tweets_list:
        tweets_json.append(json.dumps(tweet.tweet_json))
    context = {'tweets_json': tweets_json,
               'entities_list': entities_list}
    return render(request, 'twitter_services/main.html', context)


def tweets_filter_entity(request, entity):
    tweets_all = Tweet.objects.all()
    tweets_filtered = []
    for tweet in tweets_all:
        for entity_dimension_pair in tweet.tweet_reputation_dimension_set.all():
            if entity == entity_dimension_pair.entity:
                tweets_filtered.append(tweet)
                break
    # TODO: create a new template page, figure out how to pass dimension to it
    context = {'tweets_filtered': tweets_filtered}
    return render(request, 'twitter_services/filter_entities.html', context)