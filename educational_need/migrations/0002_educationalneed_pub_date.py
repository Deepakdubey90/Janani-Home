# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-01 21:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('educational_need', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationalneed',
            name='pub_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
