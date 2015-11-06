from django.shortcuts import render
from .models import Tweet, Tweet_Reputation_Dimension
import json

# TODO: find a clever approach for the block below
entities_set = Tweet_Reputation_Dimension.objects.all().values('entity').distinct()
entities_list = []
for item in entities_set:
    entities_list.append(item['entity'])

dimension_set = Tweet_Reputation_Dimension.objects.all().values('dimension').distinct()
dimension_list = []
for item in dimension_set:
    dimension_list.append(item['dimension'])


# Create your views here.
def main(request):
    tweets_json = []

    for tweet in Tweet.objects.all():
        tweet_json = json.loads(tweet.tweet_json)
        tweet_json['reputation_dimension'] \
            = ', '.join('%s: %s' % (rep.entity, rep.dimension)
                                for rep in tweet.tweet_reputation_dimension_set.all())
        tweets_json.append(json.dumps(tweet_json))
    context = {'tweets': tweets_json,
               'entities_list': entities_list,
               }
    return render(request, 'twitter_services/main.html', context)


def tweets_filter_entity(request, entity):
    tweets_filtered = []

    for tweet in Tweet.objects.all():
        for entity_dimension_pair in tweet.tweet_reputation_dimension_set.all():
            if entity == entity_dimension_pair.entity:
                tweet_json = json.loads(tweet.tweet_json)
                tweet_json['reputation_dimension'] \
                    = ', '.join('%s: %s' % (rep.entity, rep.dimension)
                                for rep in tweet.tweet_reputation_dimension_set.all())
                tweets_filtered.append(json.dumps(tweet_json))
                continue
    context = {'tweets': tweets_filtered,
               'entity': entity,
               'entities_list': entities_list,
               'dimension_list': dimension_list
               }
    return render(request, 'twitter_services/filter_entity.html', context)