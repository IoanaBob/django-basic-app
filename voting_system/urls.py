from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.post_list, name='post_list'),
    #url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    #url(r'^post/new/$', views.post_new, name='post_new'),
    #url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),

    #these are for the beginning test db, leave them here for now
    url(r'^test/$', views.test, name='test'),
    url(r'^post/new/$', views.post_new, name='post_new'),

    #admin interface
    url(r'^regions/$', views.regions, name='regions'),
]