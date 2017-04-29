from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from coreExtend import views as core_views

admin.autodiscover()
admin.site.site_header = 'ulost.net'

urlpatterns = [
    url(r'^admin96/', include(admin.site.urls)),
    url(r'^', include('coreExtend.urls', namespace='CoreExtend')),
    url(r'^', include('redirection.urls', namespace='Redirection')),

    #Static
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="Index_page"),
    url(r'^404/$', TemplateView.as_view(template_name="404.html"), name="404_page"),
	url(r'^500/$', TemplateView.as_view(template_name="500.html"), name="500_page"),
	url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
	url(r'^humans\.txt$', TemplateView.as_view(template_name="humans.txt", content_type='text/plain')),

    #API
    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
	#url(r'^api/v1/', include('redirection.api', namespace='RedirectionAPI')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
