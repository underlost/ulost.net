# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 13:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreExtend', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Account', 'verbose_name_plural': 'Accounts'},
        ),
    ]