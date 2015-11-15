from django.db import models
from django.utils import timezone

# Create your models here.
# Extra fields to be added in the json file: entity, reputation_dimension, sentiment_score


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key=True, default='Undefined: ' + str(timezone.now()))
    tweet_json = models.TextField()

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet_id


# Table to store training set of tweets
class TweetTrainingSet(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key=True, default='Undefined: ' + str(timezone.now()))
    tweet_json = models.TextField()

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet_id