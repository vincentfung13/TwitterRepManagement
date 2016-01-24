from django.conf.urls import include, url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^entity/(?P<entity>.*)/$', login_required(views.TweetsFilter.as_view()), name='tweets_filtered_entity'),
    url(r'^entity_dimension/(?P<entity>.*)/(?P<dimension>.*)/$',
        login_required(views.TweetsFilter.as_view()),
        name='tweets_filtered_entity_dimension'),
]
