from django.shortcuts import render
from .models import Tweet, Tweet_Reputation_Dimension, Tweet_Training
import tweet_classifier
import json


entities_list = [item['entity'] for item in Tweet_Reputation_Dimension.objects.values('entity').distinct()]
dimension_list = [dimension['dimension']
                  for dimension in Tweet_Reputation_Dimension.objects.values('dimension').distinct()]


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


def tweets_filter(request, entity, dimension=None):
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

    if dimension is not None:
        tweets_filtered = [tweet for tweet in tweets_filtered if entity_dimension_match(tweet, entity, dimension)]

    context = {'tweets': tweets_filtered,
               'entity': entity,
               'entities_list': entities_list,
               'dimension_list': dimension_list,
               'Dimension': dimension
               }
    return render(request, 'twitter_services/tweets_filter.html', context)


# Helper function for filtering with entity and dimension
def entity_dimension_match(tweet, entity, dimension):
    tweet_id = json.loads(tweet).get('id_str')
    for obj in Tweet_Reputation_Dimension.objects.filter(tweet__tweet_id=tweet_id):
        if obj.entity == entity and obj.dimension == dimension:
            return True
    return False
