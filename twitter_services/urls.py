from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^entity/(?P<entity>.*)/$', views.TweetsFilter.as_view(), name='tweets_filtered_entity'),
    url(r'^entity_dimension/(?P<entity>.*)/(?P<dimension>.*)/$',
        views.TweetsFilter.as_view(), name='tweets_filtered_entity_dimension'),
]
