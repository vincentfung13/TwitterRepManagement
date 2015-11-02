# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_services', '0004_auto_20151101_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='id',
        ),
        migrations.AddField(
            model_name='tweet',
            name='tweet_id',
            field=models.CharField(default=b'Undefined: 2015-11-01 21:50:35.282866+00:00', max_length=50, serialize=False, primary_key=True),
        ),
    ]
