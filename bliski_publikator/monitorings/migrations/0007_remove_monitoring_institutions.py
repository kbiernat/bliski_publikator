# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 00:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitorings', '0006_monitoring_max_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoring',
            name='institutions',
        ),
    ]