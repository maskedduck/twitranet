from django.conf.urls.defaults import *
from django.contrib import admin
from core.views import *
import os.path

static_content = os.path.join (os.path.dirname(__file__), "looknfeel", "static")

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^twitranet/', include('twitranet.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^$', homepage, name="homepage"),

	(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': static_content }),
	(r'^favicon.ico$', 'django.views.static.serve', {'document_root': static_content, 'path':'favicon.ico'}),

    # user auth views
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',name="login"),
    url(r'^accounts/logout/$', logout_view,name="logout"),

    # admin urls
    url(r'^admin/', include(admin.site.urls),name='admin'),
)
