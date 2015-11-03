# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('tweet_id', models.CharField(default=b'Undefined: 2015-11-03 16:45:58.301546+00:00', max_length=50, serialize=False, primary_key=True)),
                ('tweet_json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tweet_Reputation_Dimension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(max_length=50)),
                ('dimension', models.CharField(max_length=20)),
                ('tweet', models.ForeignKey(to='twitter_services.Tweet')),
            ],
        ),
    ]
