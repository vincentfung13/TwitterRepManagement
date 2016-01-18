from user_handle import views
from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^login/$', views.Login.as_view(), name='Login'),
    url(r'^logout/$', views.Logout.as_view(), name='Logout'),
    url(r'^(?P<username>\w+)/$', views.Index.as_view(), name='Index'),
]
