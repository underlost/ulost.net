from django.conf.urls import *
from . import views

urlpatterns = patterns('',
	url(r'^(?P<slug>[-\w]+)/$', views.LinkRedirect, name = 'link_redirect'),
)
