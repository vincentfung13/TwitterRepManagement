# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_services', '0005_auto_20151101_2150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='repustiaon_category',
            new_name='reputation_category',
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_id',
            field=models.CharField(default=b'Undefined: 2015-11-02 16:10:54.072138+00:00', max_length=50, serialize=False, primary_key=True),
        ),
    ]
