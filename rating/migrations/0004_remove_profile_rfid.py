# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-11 19:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0003_auto_20171211_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='rfid',
        ),
    ]