from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    'grumers.apps.web.views',
    # catch all
    url(r'^(?P<url>.*)$',
        views.GenericPageView.as_view(),
        name='web_page',
        ),
    url(r'^$',
        views.GenericPageView.as_view(),
        name='web_home',
        kwargs={'url': ''}
        ),
)
