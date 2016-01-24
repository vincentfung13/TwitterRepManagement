from user_handle import views
from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^login/$', views.Login.as_view(), name='Login'),
    url(r'^logout/$', views.Logout.as_view(), name='Logout'),
    url(r'^(?P<username>\w+)/$', views.Index.as_view(), name='Index'),
    url(r'^(?P<username>\w+)/interest/$', views.ManageInterested.as_view(), name='Interests'),
    url(r'^(?P<username>\w+)/interest/(?P<action>\w+)/$', views.ManageInterested.as_view(), name='ManageInterests'),
    url(r'^(?P<username>\w+)/inbox/$', views.MessageInbox.as_view(), name='MessageInbox'),
    url(r'^(?P<username>\w+)/message/(?P<message_id>[0-9]+)/$', views.MessageView.as_view(), name='Message'),
]
