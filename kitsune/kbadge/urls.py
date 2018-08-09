from django.conf.urls import patterns, url

from kitsune.kbadge import views  # noqa


urlpatterns = patterns(
    '',
    url(r'^$', views.badges_list, name='kbadge.badges_list'),
    url(r'^awards/?$', views.awards_list, name='kbadge.awards_list'),
    url(r'^badge/(?P<slug>[^/]+)/awards/(?P<id>\d+)/?$', views.award_detail,
        name='kbadge.award_detail'),
    url(r'^badge/(?P<slug>[^/]+)/?$', views.detail,
        name='kbadge.detail'),
)
