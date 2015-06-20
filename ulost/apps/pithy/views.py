from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from .models import SiteLink, ClickLink, BlockedIp

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

class LinkListView(ListView):
	paginate_by = 25
	template_name = 'linklist.html'

	def get_queryset(self):
		links = SiteLink.objects.order_by('-pub_date')
		return links

	def get_context_data(self, **kwargs):
		context = super(LinkListView, self).get_context_data(**kwargs)
		return context

class BlockedListView(ListView):
	paginate_by = 25
	template_name = 'blockedlist.html'

	def get_queryset(self):
		blocked = BlockedIp.objects.order_by('name')
		return blocked

	def get_context_data(self, **kwargs):
		context = super(BlockedListView, self).get_context_data(**kwargs)
		return context
