from django.conf.urls import patterns, url

from iapp_user import views

urlpatterns = patterns('',
    url(r'^edit/$', views.edit, name='user_new'),
    url(r'^edit/(?P<uid>[-\w]+)/$', views.edit, name='user_edit'),
    url(r'^(?P<uid>[-\w]+)/$', views.detail, name='user_detail'),
    url(r'^$', views.index, name='index'),
)
