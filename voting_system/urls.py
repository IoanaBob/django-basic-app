from django.conf.urls import url
from voting_system import views

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
    url(r'^regions/populate$', views.populate_regions, name='populate_regions'),

    # candidates pages CRUD
    url(r'^candidates/$', views.candidates, name='candidates'),

    url(r'^candidates/create/$', views.candidate_create, name='candidate_create'),
    url(r'^candidates/edit/(?P<id>\d+)/$', views.candidate_edit, name='candidates_edit'),
    url(r'^candidates/delete/(?P<id>\d+)/$', views.candidate_delete, name='candidate_delete'),
    
    # elections pages CRUD
    url(r'^elections/$', views.elections, name='elections'),
	url(r'^elections/create/$', views.election_create, name='election_create'),
    url(r'^elections/edit/(?P<id>\d+)/$', views.election_edit, name='election_edit'),
    url(r'^elections/delete/(?P<id>\d+)/$', views.election_delete, name='election_delete'),

    # roles pages CRUD
    url(r'^roles/$', views.roles, name='roles'),
    url(r'^roles/create/$', views.role_create, name='role_create'),
    url(r'^roles/edit/(?P<id>\d+)/$', views.role_edit, name='role_edit'),
    url(r'^roles/delete/(?P<id>\d+)/$', views.role_delete, name='role_delete'),

    #voter interface
    url(r'^$', views.homepage, name='homepage'),
]