from django.conf.urls import patterns, url

from iapp_user import views

urlpatterns = patterns('',
    url(r'^edit/$', views.edit, name='user_new'),
    url(r'^edit/(?P<uid>[-\w]+)/$', views.edit, name='user_edit'),
    url(r'^(?P<uid>[-\w]+)/$', views.details, name='user_details'),
    url(r'^$', views.index, name='user_index'),
)
