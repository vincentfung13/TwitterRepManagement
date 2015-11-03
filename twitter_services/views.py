from django.shortcuts import render
from .models import Tweet
import json

# Create your views here.
def main(request):
    tweets_list = Tweet.objects.all()
    tweets_json = []
    tweets_category = []
    for tweet in tweets_list:
        tweets_json.append(json.dumps(tweet.tweet_json))
        tweets_category.append(tweet.reputation_category)
    context = {'tweets_json': tweets_json,
               'tweets_category': tweets_category}
    return render(request, 'twitter_services/main.html', context)