# Configure
import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'

from twitter_services.models import Tweet

tweets = Tweet.objects.all()
for item in tweets:
    print tweets