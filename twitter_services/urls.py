from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'main/$', views.main, name='main'),
    url(r'^entity/(?P<entity>.*)/$', views.tweets_filter, name='tweets_filtered_entity'),
    url(r'^entity_dimension/(?P<entity>.*)/(?P<dimension>.*)/$',
        views.tweets_filter, name='tweets_filtered_entity_dimension'),
]
