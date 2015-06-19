import os
import urllib2
from urlparse import urlparse
import datetime
from time import strftime
from hashlib import md5
import uuid

from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.encoding import smart_unicode, smart_str

def guid_generator(user_id=None, length=32):
	if user_id:
		guid_base = "%s" % (user_id)
		guid_encode = guid_base.encode('ascii', 'ignore')
		guid = md5(guid_encode).hexdigest()[:12]
	else:
		guid_base = str(uuid.uuid4())
		guid_encoded = guid_base.encode('ascii', 'ignore')
		guid = md5(guid_encoded).hexdigest()[:length]
	return guid
