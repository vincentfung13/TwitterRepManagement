# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_services', '0003_remove_tweet_tweet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='repustiaon_category',
            field=models.TextField(),
        ),
    ]
