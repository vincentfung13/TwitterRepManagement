from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'main', views.main, name='main'),
    url(r'^entity/(?P<entity>RL([0-9]|[A-Z])+)/', views.tweets_filter_entity, name='tweets_filtered_entity'),
]
