from __future__ import absolute_import
from django.contrib import admin
from django.db import models
from .models import SiteLink, ClickLink, BlockedIp

class SiteLink(admin.ModelAdmin):
    list_display = ('user', 'link', 'pub_date' )
    list_filter = ('user')
    exclude = ('note_html',)

class ClickLinkAdmin(admin.ModelAdmin):
    search_fields = ('link', 'referer', 'ip_addr' )
    list_display = ('link', 'referer', 'ip_addr', 'pub_date', 'user_agent')

class BlockedIpAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_addr')
    list_filter = ('name', 'ip_addr')

admin.site.register(SiteLink, SiteLinkAdmin)
admin.site.register(ClickLink, ClickLinkAdmin)
admin.site.register(BlockedIp, BlockedIpAdmin)
