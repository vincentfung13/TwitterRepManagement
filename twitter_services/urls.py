from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'main/$', views.main, name='main'),
    url(r'^entity/(?P<entity>RL([0-9]|[A-Z])+)/$', views.tweets_filter, name='tweets_filtered_entity'),
    url(r'^entity/(?P<entity>RL([0-9]|[A-Z])+)/(?P<dimension>.*)/$',
        views.tweets_filter, name='tweets_filtered_entity_dimension'),
    url(r'classify/$', views.tweet_classification, name='tweet_classification')
]
