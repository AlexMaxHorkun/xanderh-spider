# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import xanderhorkunspider.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebsitesModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('host', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'websites',
            },
            bases=(xanderhorkunspider.models.Website, models.Model),
        ),
    ]
