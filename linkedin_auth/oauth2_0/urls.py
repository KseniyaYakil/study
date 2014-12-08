from django.conf.urls import patterns, url
from oauth2_0 import views

urlpatterns = patterns('',
	url(r'^$', views.oauth20, name='auth20_page'),
	url(r'^conns/$', views.connections, name='user_connections'),
	url(r'^conns/(?P<conn_id>\d+)/$', views.connect_info, name='user_conn_info'),
)
