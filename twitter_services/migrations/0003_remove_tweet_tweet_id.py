# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_services', '0002_auto_20151101_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='tweet_id',
        ),
    ]
