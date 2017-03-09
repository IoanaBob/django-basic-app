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
    url(r'^candidates/$', views.candidates, name='candidates'),
    url(r'^candidates/create/$', views.newCandidate, name='newCandidate'),
    url(r'^candidates/edit/(?P<id>\d+)/$', views.editCandidate, name='editCandidates'),
    url(r'^candidates/delete/(?P<id>\d+)/$', views.deleteCandidate, name='DeleteCandidate'),
    url(r'^elections/$', views.elections, name='elections'),
	url(r'^elections/create/$', views.election_create, name='election_create'),
    url(r'^elections/edit/$', views.election_edit, name='election_edit'),
    url(r'^elections/delete/$', views.election_delete, name='election_delete'),
    url(r'^regions/populate$', views.populate_regions, name='populate_regions')

]