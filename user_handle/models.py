from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from twitter_services.models import Tweet


# This model represents the message that is sent to the user
class Message(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    entity = models.CharField(max_length=30)
    reputation_dimension = models.CharField(max_length=30, blank=True)
    topic_str = models.TextField(blank=True)
    tweet = models.ManyToManyField(Tweet)
    read = models.BooleanField(default=False)


# This model represents the relation between users and the certain entities they are interested in
class UserEntity(models.Model):
    user = models.ForeignKey(User)
    entity = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = ['user', 'entity']


# This model is an abstraction of users' inbox
class UserMessage(models.Model):
    user = models.ForeignKey(User)
    message = models.ManyToManyField(Message)
