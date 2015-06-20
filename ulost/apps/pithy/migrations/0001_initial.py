# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedIp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, blank=True)),
                ('ip_addr', models.GenericIPAddressField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClickLink',
            fields=[
                ('guid', models.UUIDField(default=b'1b7fe1f73fb88be5d0717fc5095ae480', serialize=False, editable=False, primary_key=True)),
                ('referer', models.CharField(max_length=512, null=True)),
                ('user_agent', models.CharField(max_length=1024, null=True)),
                ('ip_addr', models.GenericIPAddressField(null=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='SiteLink',
            fields=[
                ('guid', models.UUIDField(default=b'7ce7795a448284ab6855a1922965c8a7', serialize=False, editable=False, primary_key=True)),
                ('link', models.URLField(max_length=512)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True, max_length=512, blank=True)),
                ('note', models.TextField(verbose_name='body', blank=True)),
                ('note_html', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='clicklink',
            name='link',
            field=models.ForeignKey(to='pithy.SiteLink', null=True),
        ),
    ]
