from django.db import models
from django.core.cache import cache
from django.conf import settings
from coreExtend.models import Account

from .utils import guid_generator
from .models import *

class BlockedManager(models.Manager):

    def get_ips(self):
        """
        Returns a cached list of ip addresses
        """
        result = cache.get(BLOCKED_IPS_LIST, None)

        if not result:
            result = self.values_list('ip_addr', flat=True)
            cache.set(BLOCKED_IPS_LIST, result, 60*60*24) # 1 day

        return result
