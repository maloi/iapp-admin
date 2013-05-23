from django.conf.urls import patterns, url

from iapp_group import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cn>[-\w]+)/$', views.group, name='group'),
    url(r'^edit/$', views.group_edit, name='group_new'),
    url(r'^edit/(?P<cn>[-\w]+)/$', views.group_edit, name='group_edit'),
)