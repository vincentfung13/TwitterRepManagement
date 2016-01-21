from django.db import models
from django.contrib.auth.models import User
from twitter_services.models import Tweet


# This model represnets the message that is sent to the user
class Message(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    entity = models.CharField(max_length=30)
    message = models.TextField()
    tweets = models.ManyToManyField(Tweet)


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

    def add_message(self, entity, tweets):
        print 'I am called! %s' % entity