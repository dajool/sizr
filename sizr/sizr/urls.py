# -*- coding: utf-8 -*-

__author__ = 'Jochen Breuer <brejoc@gmail.com>'
__copyright__ = 'Jochen Breuer <brejoc@gmail.com>'
__license__ = 'BSD 3-Clause License'

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sizr.views.home', name='home'),
    # url(r'^sizr/', include('sizr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^resize/(?P<url>[-\w]+)/$','image_sizr.views.resize', name="image_resize"),
    # url(r'^thumbnail/(?P<url>[0-9A-Za-z]+)/(?P<x>\d+)/(?P<y>\d+)/$','image_sizr.views.resize', name="image_resize"),
    url(r'^thumbnail/(?P<url>[-\w]+)/(?P<x>\d+)/(?P<y>\d+)/$','image_sizr.views.resize', name="image_resize"),
    # url(r'^one/$', RedirectView.as_view(url='//'), name='image_redirect'),
)


urlpatterns += patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    )

if settings.DEBUG:
    # route for upload folder in debug
    urlpatterns += patterns('',
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

    urlpatterns += patterns('',
        url(r'^bucket/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.BUCKET_ROOT,
        }),
    )

    # route for static files folder in debug
    urlpatterns += staticfiles_urlpatterns()
