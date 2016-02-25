from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.aggregates import ArrayAgg

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


# Table for statistics, the front end will use the data in this table to draw graphs
class Statistics(models.Model):
    related_entity = models.CharField(max_length=20, default='Undefined')
    reputation_dimension = models.CharField(max_length=20, default='Whole')
    timestamp = models.DateField(default=timezone.now)
    total_tweets_count = models.IntegerField(default=0)
    negative_count = models.IntegerField(default=0)
    # This attribute takes into account of how negative each tweets are
    reputation_score = models.FloatField(default=0)
