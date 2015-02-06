# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import xanderhorkunspider.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoadingModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('success', models.BooleanField(default=False)),
                ('headers_serialized', models.CharField(max_length=4096)),
                ('content', models.CharField(max_length=1024000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('loading_time', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'loadings',
            },
            bases=(models.Model, xanderhorkunspider.models.Loading),
        ),
        migrations.CreateModel(
            name='PageModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'pages',
            },
            bases=(models.Model, xanderhorkunspider.models.Page),
        ),
        migrations.CreateModel(
            name='WebsitesModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'websites',
            },
            bases=(models.Model, xanderhorkunspider.models.Website),
        ),
        migrations.AddField(
            model_name='pagemodel',
            name='website',
            field=models.ForeignKey(related_name='pages_set', to='websites.WebsitesModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loadingmodel',
            name='page',
            field=models.ForeignKey(related_name='loadings_set', to='websites.PageModel'),
            preserve_default=True,
        ),
    ]
