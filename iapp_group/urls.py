from django.conf.urls import patterns, url
from iapp_group import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)