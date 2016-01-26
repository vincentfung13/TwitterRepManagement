from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

# Create your models here.
# Extra fields to be added in the json file: related_entity, reputation_dimension, sentiment_score


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key=True, default='Undefined: ' + str(timezone.now()))
    tweet = JSONField(default={'message': 'undefined'})
    created_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet['id_str']


# Table to store training set of tweets
class TweetTrainingSet(models.Model):
    tweet = JSONField(default={'message': 'undefined'})

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet['id_str']
