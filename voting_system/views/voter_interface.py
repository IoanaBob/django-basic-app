from django.shortcuts import render
from voting_system.models import VoterCode, VoterAuth, RegionVote, Verify
from voting_system.forms import CheckPasswordForm, CheckCodeForm, RegisterVoteForm, VerifyLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
import json
import uuid
from django.db import connections
from django.contrib.auth.hashers import make_password, check_password as password_check
from django.contrib import messages

def public_homepage(request):

	return render(request, 'voter_interface/pages/homepage.html', {"title": "Homepage", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ]})

def RegisterSummary(request): #CHRIS PLEASE CHECK
	return render(request, 'voter_interface/pages/voting/register_summary.html', {"title": "Register to Vote Online - Summary", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ],'destination':request.GET.get('destination') })

def RegisterVoterId(request): #Chris Please Check

	return render(request, 'voter_interface/pages/voting/register_voter_id.html', {"title": "Register to Vote Online - Enter Voter Id", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] })


def public_verify(request):
	if request.method == "POST":
		form = VerifyLoginForm(request.POST)
		if form.is_valid():
			try:
				user = Verify.objects.get(email = request.POST.get('email'))
				if user is not None:
					# WE NEED TO REMOVE THIS SESSION AFTER TIME and WE NEED TO OFFER LOGOUT
					if  password_check(request.POST.get('password'),user.password_hash):
						request.session['verify_username'] = user.email
						request.session['verify_forename'] = user.first_name.capitalize()
						request.session['verify_surname'] = user.last_name.capitalize()
						messages.success(request, "Welcome! You have been successfully logged in!")
						return redirect (request.POST.get('destination'))
					else:
						messages.error(request, "Your credentials does not match our records.")
						form = VerifyLoginForm()
						return render(request, 'voter_interface/pages/verify.html',{'title': "GOV Verify Login", 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify'))], 'welcome': "Verify Login", 'form': form, "destination":destination})
			except Verify.DoesNotExist:
					messages.error(request, "Your credentials does not match our records.")
					form = VerifyLoginForm()
					return render(request, 'voter_interface/pages/verify.html',{'title': "GOV Verify Login", 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify'))], 'welcome': "Verify Login", 'form': form, "destination":destination})
		#COPIED CODE HAD NO 'ELSE' HERE - WHAT DO WE WANT TO DO

	else:
		form = VerifyLoginForm()
		destination = request.GET.get('destination')
		return render(request, 'voter_interface/pages/verify.html',{'title': "GOV Verify Login", 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify'))], 'welcome': "Verify Login", 'form': form, "destination":destination})

#CAST VOTE
def CastVoteSummary(request): #CHRIS PLEASE CHECK
	return render(request, 'voter_interface/pages/voting/cast_vote_summary.html', {"title": "Cast Your Vote- Summary", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ],'destination':request.GET.get('destination') })

def CastVoteId(request): #Chris Please Check

	return render(request, 'voter_interface/pages/voting/cast_vote_id.html', {"title": "Register to Vote Online - Enter Voter Id", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] })



def public_vote_home(request):

	return render(request, 'voter_interface/pages/voting/home.html', {"title": "Election Homepage","header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home') )]})


def public_vote_ballot(request):
	if request.method == "POST":
		#if checks passed
		return render(request, 'voter_interface/pages/voting/ballot.html', {"title": "Election Ballot", "acknowledgement": True, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Home', reverse('public_vote__ballot'))]})

	else:
		return render(request, 'voter_interface/pages/voting/ballot.html', {"title": "Election Ballot", "header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Home', reverse('public_vote__ballot'))]})



def public_vote_request(request):
	if request.method == "POST":

		#checks

		#if checks passed
		return render(request, 'voter_interface/pages/voting/request.html', {"title": "Request to Vote", "sent": True,'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home') ), ('Request Code', reverse('public_vote__request_code') ),("Sent", "#")]})
	else:
		#FRONT END GUYS, LOOK AT THE STRUCTURE,  breadcrumb is the menu, title is the page title, header_messages are the welcome message
		return render(request, 'voter_interface/pages/voting/request.html', {
			"title": "Request to Vote",
			'breadcrumb': [
				('Home', "http://www.gov.uk"),
				('Elections', reverse('public_homepage')),
				('Log In', reverse('public_verify')),
				('Election Home', reverse('public_vote__home') ),
				('Election Home', reverse('public_vote__request_code'))
			]
			})


def SecureVoteToDatabse(vote_instance,region_id):
	region_db_name = "region"+str(region_id)
	cursor = connections[region_db_name].cursor()
	cursor.execute("INSERT INTO votes (id,election_id,candidate_id,ballot_id,rank) VALUES (nextval('votes_id_seq'),"+str(vote_instance.election_id)+","+str(vote_instance.candidate_id)+",'"+str(vote_instance.ballot_id)+"',"+str(vote_instance.rank)+")");


def public_vote_place(request):
	#TO DO
	# - validate request 
	# 	- logged in
	#	- verify
	#	- voter password
	#	- voter code
	# - switch template based on voting system. 
	if request.method == "POST":
		#if checks passed
		election_id = request.POST.get('election_id')
		region_id = request.POST.get('region_id')
		
		vote_data_string = request.POST.get('rank_data')
		voter_dict = json.loads(vote_data_string)
		
		ballot_id = str(uuid.uuid4().hex)

		votes = []
		for key,rank in voter_dict.items():
			new_vote = RegionVote()
			new_vote.election_id = election_id
			new_vote.candidate_id = key
			new_vote.ballot_id = ballot_id
			new_vote.rank = rank

			SecureVoteToDatabse(new_vote,region_id)
		
		
		return render(request, 'voter_interface/pages/voting/place.html', {"title": "Election Ballot", "placed": True, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Home', reverse('public_vote__ballot'))]})

	else:

		# test data TODO: get this from DB
		election_id = 1
		
		election_vote_method = "fptp" #"stv"
		
		region_id = 1

		candidates = [(1,"1first","1last","4 why address road, Pointless Town, AB1 2CD","Labour"),(2,"2first","2last","4 why address road, Pointless Town, AB1 2CD","Labour")]

		if(election_vote_method == "fptp"):
			return render(request, 'voter_interface/pages/voting/place.html', {"election_id":election_id,"region_id":region_id,"candidates":candidates, "title": "Election Ballot", "header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Ballot', reverse('public_vote__ballot')), ('Place Vote', reverse('public_vote__place_vote')) ]})
		
		elif(election_vote_method == "stv"):
			return render(request, 'voter_interface/pages/voting/place-STV.html', {"election_id":election_id,"region_id":region_id,"candidates":candidates,"title": "Election Ballot", "header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Ballot', reverse('public_vote__ballot')), ('Place Vote', reverse('public_vote__place_vote')) ]})
		
		else:
			pass #throw an error	



# This should not be allowed to be accessed in any other way than from check_password (POST)
# when it's working
def check_code(request):
	if request.method == "POST":
		form = CheckCodeForm(request.POST)
		# SHOULD BE CHANGED TO voter id!! (when it exists)
		voter_id = form.data['id']
		code = form.data['code']
		try:
			#id should be changed to voter_id - the query - when it exists
			if code == VoterCode.objects.get(id= voter_id).code :
				return redirect('cast_vote')
		except VoterCode.DoesNotExist:
			# error message should be added here
			return redirect('check_code')	
	else:
		form = CheckCodeForm()
	return render(request, 'voter_interface/check_code.html', {'form': form})


def check_password(request):
	if request.method == "POST":
		form = CheckPasswordForm(request.POST)
		# SHOULD BE CHANGED TO voter id!! (when it exists)
		voter_id = form.data['id']
		password = form.data['password_hash']
		# password should be encrypted here
		try:
			#id should be changed to voter_id - the query - when it exists
			if password == VoterAuth.objects.using('voterauth').get(id= voter_id).password_hash :
				return redirect('check_code')
		except VoterAuth.DoesNotExist:
			# error message should be added here
			return redirect('check_password')

	else:
		form = CheckPasswordForm()
	return render(request, 'voter_interface/check_password.html', {'form': form})

# This should not be allowed to be accessed in any other way than from check_for_code (POST)
# when it's working
def cast_vote(request):
	return render(request, 'voter_interface/cast_vote.html')

def CastVote(request):
	#TO DO
	# - pass election details
	# - validate request 
	# 	- logged in
	#	- verify
	#	- voter password
	#	- voter code
	# - switch template based on voting system. 

	return render(request, 'voter_interface/ballot_paper_fptp.html')


def register_to_vote(request):
	if request.method == "POST":
		form = RegisterVoteForm(request.POST)
		# find out how to encrypt the password
		if form.is_valid():
			voter_authentihication = form.save(commit=False)
			voter_authentihication.save(using='voterauth')
			return redirect('public_homepage')
	else:
		form = RegisterVoteForm()
	return render(request, 'voter_interface/register_to_vote.html', {'form': form})



def PostcodeToConstituency(post_code):
	api_key = "HC5M9UCFwzLeEFNEguDWKe4V"
	api_url = 'https://www.theyworkforyou.com/api/getConstituency?postcode={0}&key={1}'
	constituency_json = requests.get(url=api_url.format(post_code,api_key)).json()
	
	if("name" in constituency_json):
		return constituency_json["name"]
	else:
		return None


def PostcodeToRegion(post_code,region_type="parliamentary_constituency"):
	api_url = 'https://api.postcodes.io/postcodes/{1}'
	postcode_json = requests.get(url=api_url.format(post_code)).json()
	
	if(region_type in postcode_json):
		return postcode_json[region_type]
	else:
		return None

		