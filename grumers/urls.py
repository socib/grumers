from django.conf.urls.static import static
from django.conf.urls import patterns, include
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('')

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    '',
    (r'^localeurl/', include('localeurl.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^data/', include('grumers.apps.data.urls')),
    (r'^login/?$', 'django.contrib.auth.views.login'),
    (r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
    (r'^password/', include('password_reset.urls')),
    (r'^', include('grumers.apps.web.urls')),
)
