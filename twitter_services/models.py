from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
# Extra fields to be added in the json file: related_entity, reputation_dimension, sentiment_score


class Tweet(models.Model):
    tweet = JSONField()
    # reputation_dimension = models.CharField(max_length=30, blank=True)
    # sentiment_score = models.CharField(max_length=10, blank=True)
    # related_entity = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet['id_str']


# Table to store training set of tweets
class TweetTrainingSet(models.Model):
    tweet = JSONField()

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet['id_str']
