from user_handle import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='Register'),
    url(r'^login/$', views.Login.as_view(), name='Login'),
    url(r'^logout/$', views.Logout.as_view(), name='Logout'),
    url(r'^$', login_required(views.Index.as_view()), name='Index'),
    url(r'^interest/$', login_required(views.ManageInterested.as_view()), name='Interests'),
    url(r'^inbox/$', login_required(views.MessageInbox.as_view()), name='MessageInbox'),
    url(r'^message/(?P<message_id>[0-9]+)/$',
        login_required(views.MessageView.as_view()),
        name='Message'),
]
