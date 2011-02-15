from django.conf.urls.defaults import *
from django.contrib import admin
from settings import MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'static.views.index', name="index"),	
	
	(r'^admin/', include(admin.site.urls)),
	(r'^media-manager/', include('mediamanager.urls')),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':MEDIA_ROOT, 'show_indexes':True}),
)
