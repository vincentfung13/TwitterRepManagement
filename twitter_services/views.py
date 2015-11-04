from django.shortcuts import render
from .models import Tweet
import json

# Create your views here.
def main(request):
    tweets_list = Tweet.objects.all()
    tweets_json = []
    for tweet in tweets_list:
        tweets_json.append(json.dumps(tweet.tweet_json))
    context = {'tweets_json': tweets_json}
    return render(request, 'twitter_services/main.html', context)