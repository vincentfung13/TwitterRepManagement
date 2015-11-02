from django.db import models
from django.utils import timezone

# Create your models here.
class Tweet(models.Model):
    tweet_id = models.CharField(max_length = 50, primary_key = True, default = 'Undefined: '+ str(timezone.now()))
    tweet_json = models.TextField()
    reputation_category = models.TextField()
    #sentiment = models.CharField(max_length = 10)

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet_id
