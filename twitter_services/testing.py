# Configure
import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'

from twitter_services.models import Tweet, TweetEntityDimension
from TwitterRepManagement import settings
import django
import os

from django.conf import settings

tweets = Tweet.objects.all()
for item in tweets:
    print tweets