from django.db import models
from django.contrib.auth.models import User


# This model represents the relation between users and the certain entities they are interested in
class UserEntity(models.Model):
    user = models.ForeignKey(User)
    entity = models.CharField(max_length=30, blank=True)
