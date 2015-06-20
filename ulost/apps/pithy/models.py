import markdown
import bleach

from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from coreExtend.models import Account
from .utils import guid_generator
from .managers import BlockedManager

BLOCKED_IPS_LIST = 'Pithy:blocked-ips'

class SiteLink(models.Model):
    guid = models.UUIDField(primary_key=True, max_length=32, default=guid_generator(length=32), editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    link = models.URLField(max_length=512)
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=512, blank=True, unique=True)
    note = models.TextField(_('body'), blank=True)
    note_html = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = guid_generator(length=8)
        if self.note:
            self.note_html = bleach.clean(markdown.markdown(smart_unicode(self.note)))
        super(SiteLink, self).save(*args, **kwargs)

class ClickLink(models.Model):
    guid = models.UUIDField(primary_key=True, max_length=32, default=guid_generator(length=32), editable=False)
    link = models.ForeignKey(SiteLink, null=True)
    referer = models.CharField(max_length=512, null=True)
    user_agent = models.CharField(max_length=1024, null=True)
    ip_addr = models.IPAddressField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def store(self, request):
        ip_addr = request.META['REMOTE_ADDR']
        user_agent = request.META.get('HTTP_USER_AGENT','')

        if ip_addr in BlockedIp.objects.get_ips():
            return None

        self.referer = request.META.get('HTTP_REFERER','')
        self.user_agent = user_agent
        self.ip_addr = ip_addr
        self.save()

    class Meta:
        ordering = ("-pub_date",)

class BlockedIp(models.Model):
    name = models.CharField(max_length=128, blank=True)
    ip_addr = models.IPAddressField(null=True)
    objects = BlockedManager()

    def __unicode__(self):
        return self.ip_addr

    def save(self, *args, **kwargs):
        cache.delete(BLOCKED_IPS_LIST)
        super(BlockedIp, self).save(*args, **kwargs)
