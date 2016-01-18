from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
# Extra fields to be added in the json file: entity, reputation_dimension, sentiment_score


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key=True, default='Undefined: ' + str(timezone.now()))
    json_str = models.TextField()
    reputation_dimension = models.CharField(max_length=30, blank=True)
    sentiment_score = models.CharField(max_length=10, blank=True)
    related_entity = models.CharField(max_length=30, blank=True)
    # cluster = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet_id


# Table to store training set of tweets
class TweetTrainingSet(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key=True, default='Undefined: ' + str(timezone.now()))
    json_str = models.TextField()

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet_id
