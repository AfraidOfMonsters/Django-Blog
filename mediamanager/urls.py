from django.conf.urls.defaults import *

urlpatterns = patterns('mediamanager',
	url(r'^upload/$', 'views.upload_media', name='mediamanager_upload'),
	url(r'^view/(?P<id>\d+)/$', 'views.view_media', name='mediamanager_view'),
)