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
   

     #Home
    url(r'^administration/$', views.admin_homepage, name='admin_homepage'),
    url(r'^administration/login/', views.admin_login, name='admin_login'),
    url(r'^administration/logout/$', views.admin_logout, name='admin_logout'),

    #admin interface
    url(r'^administration/regions/$', views.regions, name='regions'),
    url(r'^administration/regions/populate$', views.populate_regions, name='populate_regions'),

    # candidates pages CRUD
    url(r'^administration/candidates/$', views.candidates, name='candidates'),
    
    url(r'^administration/candidates/create/$', views.candidate_create, name='candidate_create'),
    url(r'^administration/candidates/edit/(?P<id>\d+)/$', views.candidate_edit, name='candidate_edit'),
    url(r'^administration/candidates/delete/(?P<id>\d+)/$', views.candidate_delete, name='candidate_delete'),
    
    # elections pages CRUD
    url(r'^administration/elections/$', views.elections_homepage, name='elections_homepage'),
    url(r'^administration/elections/view/$', views.elections, name='elections'),
    url(r'^administration/elections/create/$', views.election_create, name='election_create'),
    url(r'^administration/elections/edit/$', views.election_edit, name='election_edit'),
    url(r'^administration/elections/delete/$', views.election_delete, name='election_delete'),
    url(r'^administration/regions/populate$', views.populate_regions, name='populate_regions'),
    
    #admins
    url(r'^administration/admins/$', views.admin_view, name='admin_users'),
    url(r'^administration/admins/edit/(?P<id>\d+)/$', views.admin_edit, name='admin_edit'),
    url(r'^administration/admins/create/$', views.admin_create, name='admin_create'),
    #login
    #url(r'^administration/login/create$', views.CreateDummyUser, name='CreateDummyUser'),
    

    # roles pages CRUD
    url(r'^administration/roles/$', views.roles, name='roles'),
    url(r'^administration/roles/create/$', views.role_create, name='role_create'),
    url(r'^administration/roles/edit/(?P<id>\d+)/$', views.role_edit, name='role_edit'),
    url(r'^administration/roles/delete/(?P<id>\d+)/$', views.role_delete, name='role_delete'),

    # party pages CRUD
    url(r'^administration/parties/$', views.party, name='party'),
    url(r'^administration/parties/create/$', views.party_create, name='party_create'),
    url(r'^administration/parties/edit/(?P<id>\d+)/$', views.party_edit, name='party_edit'),
    url(r'^administration/parties/delete/(?P<id>\d+)/$', views.party_delete, name='party_delete'),

    #voter interface

    # voter identity check
    url(r'^check_voter_code/$', views.check_code, name='check_code'),
    url(r'^check_voter_password/$', views.check_password, name='check_password'),
    url(r'^cast_vote/$', views.cast_vote, name='cast_vote'),

    # voter codes
    url(r'^administration/voter_codes/$', views.voter_codes, name='voter_codes'),
    url(r'^administration/voter_codes/populate/$', views.populate_voter_codes, name='populate_voter_codes'),
       
    #Public START
    url(r'^$', views.public_homepage, name='public_homepage'),
    url(r'^verify/$', views.public_verify, name='public_verify'),

    #cast_vote
    #url(r'^cast_vote/$', views.CastVote, name='cast_vote'),
    

    url(r'^voting/home/$', views.public_vote_home, name='public_vote__home'),
    url(r'^voting/ballot/$', views.public_vote_ballot, name='public_vote__ballot'),
    url(r'^voting/request/$', views.public_vote_request, name='public_vote__request_code'),
    url(r'^voting/place/$', views.public_vote_place, name='public_vote__place_vote')

]
