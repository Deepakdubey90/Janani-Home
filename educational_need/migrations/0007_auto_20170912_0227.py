# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-12 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educational_need', '0006_educationalneed_date_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalneed',
            name='date_uuid',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
    ]
