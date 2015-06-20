from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import SiteLink, ClickLink

def LinkRedirect(request, slug):
	obj = get_object_or_404(SiteLink, slug=slug)
	#Redirects links and keeps track of them
	try:
		outgoing_link = obj.link
		link_guid = obj.guid
		link_click = ClickLink(link=link_guid)
		link_click.store(request)
	except KeyError:
		# Someone got here without the link param
		# Redirect to Home as default
		link = '/'

	return HttpResponseRedirect(outgoing_link)
