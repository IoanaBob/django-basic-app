from django.conf.urls import url
from voting_system import views

urlpatterns = [

    #Home & login/logout
    url(r'^administration/$', views.admin_master_homepage, name='admin_master_homepage'),
    url(r'^administration/login/', views.admin_login, name='admin_login'),
    url(r'^administration/logout/$', views.admin_logout, name='admin_logout'),

    # candidates pages CRUD
   
    url(r'^administration/candidates/$', views.candidate_homepage, name='candidate_homepage'),
    url(r'^administration/candidates/view/$', views.candidate_view, name='candidate_view'),
    url(r'^administration/candidates/view/(?P<page_id>\d+)$', views.candidate_view_page, name='candidate_view_page'),
    url(r'^administration/candidates/create/$', views.candidate_create, name='candidate_create'),
    url(r'^administration/candidates/edit/(?P<id>\d+)/$', views.candidate_edit, name='candidate_edit'),
    url(r'^administration/candidates/delete/(?P<id>\d+)/$', views.candidate_delete, name='candidate_delete'),
    
    # elections pages CRUD
    url(r'^administration/elections/$', views.election_homepage, name='election_homepage'),
    url(r'^administration/elections/view/$', views.election_view, name='election_view'),
    url(r'^administration/elections/view/(?P<page_id>\d+)$', views.election_view_page, name='election_view_page'),
    url(r'^administration/elections/create/$', views.election_create, name='election_create'),
    url(r'^administration/elections/edit/(?P<id>\d+)/$', views.election_edit, name='election_edit'),
    url(r'^administration/elections/delete/(?P<id>\d+)/$', views.election_delete, name='election_delete'),
    
    #Regions
    url(r'^administration/regions/$', views.region_homepage, name='region_homepage'),
    url(r'^administration/regions/populate$', views.region_populate, name='region_populate'),
    url(r'^administration/regions/view/$', views.region_view, name='region_view'),
    url(r'^administration/regions/view/(?P<page_id>\d+)$', views.region_view_page, name='region_view_page'),
    url(r'^administration/regions/edit/(?P<id>\d+)/$', views.region_edit, name='region_edit'),
    url(r'^administration/regions/create/$', views.region_create, name='region_create'),
    url(r'^administration/regions/delete/(?P<id>\d+)/$', views.region_delete, name='region_delete'),
    
    #admins
    url(r'^administration/admins/$', views.admins_homepage, name='admin_homepage'),
    url(r'^administration/admins/view/$', views.admin_view, name='admin_view'),
     url(r'^administration/admins/view/(?P<page_id>\d+)$', views.admin_view_page, name='admin_view_page'),
    url(r'^administration/admins/edit/(?P<id>\d+)/$', views.admin_edit, name='admin_edit'),
    url(r'^administration/admins/create/$', views.admin_create, name='admin_create'),
    url(r'^administration/admins/delete/(?P<id>\d+)/$', views.admin_delete, name='admin_delete'),

    # roles pages CRUD
    url(r'^administration/roles/$', views.role_homepage, name='role_homepage'),
    url(r'^administration/roles/view/$', views.role_view, name='role_view'),
    url(r'^administration/roles/view/(?P<page_id>\d+)$', views.role_view_page, name='role_view_page'),
    url(r'^administration/roles/create/$', views.role_create, name='role_create'),
    url(r'^administration/roles/edit/(?P<id>\d+)/$', views.role_edit, name='role_edit'),
    url(r'^administration/roles/delete/(?P<id>\d+)/$', views.role_delete, name='role_delete'),

    # party pages CRUD
    url(r'^administration/parties/$', views.party_homepage, name='party_homepage'),
    url(r'^administration/parties/view/$', views.party_view, name='party_view'),
    url(r'^administration/parties/view/(?P<page_id>\d+)$', views.party_view_page, name='party_view_page'),
    url(r'^administration/parties/create/$', views.party_create, name='party_create'),
    url(r'^administration/parties/edit/(?P<id>\d+)/$', views.party_edit, name='party_edit'),
    url(r'^administration/parties/delete/(?P<id>\d+)/$', views.party_delete, name='party_delete'),

    # Voter Code CRUD
    url(r'^administration/codes/$', views.voter_code_homepage, name='voter_code_homepage'),
    url(r'^administration/codes/view/$', views.voter_code_view, name='voter_code_view'),
     url(r'^administration/codes/view/(?P<page_id>\d+)$', views.voter_code_view_page, name='voter_code_view_page'),
  

    #voter interface

    # voter identity check
    url(r'^check_voter_code/$', views.check_code, name='check_code'),
    url(r'^check_voter_password/$', views.check_password, name='check_password'),
    url(r'^cast_vote/$', views.cast_vote, name='cast_vote'),
       
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
