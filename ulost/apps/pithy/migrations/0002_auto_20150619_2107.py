# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pithy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clicklink',
            name='guid',
            field=models.UUIDField(default=b'a7033527e9726218439e775424b5a656', serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='sitelink',
            name='guid',
            field=models.UUIDField(default=b'6be03bfad3ac07b3a44a94e55b844980', serialize=False, editable=False, primary_key=True),
        ),
    ]
