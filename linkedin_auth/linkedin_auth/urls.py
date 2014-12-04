from django.conf.urls import patterns, include, url
from django.contrib import admin
from linkedin_auth import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^redirect', views.redirected, name='redirected'), 
    url(r'^oauth2_0/', include('oauth2_0.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
