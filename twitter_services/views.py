from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Tweet

# Create your views here.
def main(request):
    tweets_list = Tweet.objects.all()
    template = loader.get_template('twitter_services/main.html')
    context = {'tweets_list': tweets_list}
    return render(request, 'twitter_services/main.html', context)