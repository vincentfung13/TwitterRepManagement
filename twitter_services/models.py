from django.db import models
from django.utils import timezone

# Create your models here.


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key=True, default='Undefined: ' + str(timezone.now()))
    tweet_json = models.TextField()
    sentiment_score = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet_id


# Table to store training set of tweets
class TweetTrainingSet(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key=True, default='Undefined: ' + str(timezone.now()))
    tweet_json = models.TextField()
    sentiment_score = models.CharField(max_length=5, blank=True, null=True)

    def __unicode__(self):
        return 'tweet_id: ' + self.tweet_id


class TweetEntityDimension(models.Model):
    id = models.TextField(primary_key=True, default='Undefined: ' + str(timezone.now()))
    tweet = models.ForeignKey(Tweet)
    entity = models.CharField(max_length=50)
    dimension = models.CharField(max_length=20)

    def __unicode__(self):
        return '{ entity: %s; %s; dimension: %s;}' % (self.entity, self.tweet, self.dimension)