from django.shortcuts import render
from django.views.generic import View
from .models import Tweet
from tweet_processing import utility
import json


# Create your views here.
class Main(View):
    def get(self, request):
        tweets_json = [json.dumps(utility.build_dict(tweet)) for tweet in Tweet.objects.all().order_by('-created_at')]

        context = {
            'tweets': tweets_json,
            'entities_list': utility.entities_list
        }
        return render(request, 'twitter_services/main.html', context)


class TweetsFilter(View):
    def get(self, request, entity, dimension=None):
        if dimension is not None:
            tweets = Tweet.objects.filter(related_entity=entity, reputation_dimension=dimension).order_by('-created_at')
        else:
            tweets = Tweet.objects.filter(related_entity=entity).order_by('-created_at')

        tweets_filtered = [json.dumps(utility.build_dict(tweet)) for tweet in tweets]

        context = {
            'tweets': tweets_filtered,
            'entity': entity,
            'entities_list': utility.entities_list,
            'dimension_list': utility.dimension_list,
            'Dimension': dimension
        }

        return render(request, 'twitter_services/tweets_filter.html', context)
