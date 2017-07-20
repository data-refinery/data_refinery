# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-26 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_models', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downloaderjobstobatches',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='downloaderjobstobatches',
            name='downloader_job',
        ),
        migrations.RemoveField(
            model_name='processorjobstobatches',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='processorjobstobatches',
            name='processor_job',
        ),
        migrations.AddField(
            model_name='downloaderjob',
            name='batches',
            field=models.ManyToManyField(to='data_refinery_models.Batch'),
        ),
        migrations.AddField(
            model_name='downloaderjob',
            name='downloader_task',
            field=models.CharField(default='old', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='downloaderjob',
            name='retried',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='processorjob',
            name='batches',
            field=models.ManyToManyField(to='data_refinery_models.Batch'),
        ),
        migrations.AddField(
            model_name='processorjob',
            name='retried',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='DownloaderJobsToBatches',
        ),
        migrations.DeleteModel(
            name='ProcessorJobsToBatches',
        ),
    ]
