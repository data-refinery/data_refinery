# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyjob',
            name='success',
            field=models.NullBooleanField(),
        ),
    ]
