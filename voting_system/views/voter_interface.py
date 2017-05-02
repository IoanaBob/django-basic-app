from django.shortcuts import render
from voting_system.models import VoterCode, VoterAuth, RegionVote, Verify, Region, Election, Voter, Candidate
from voting_system.forms import CheckPasswordForm, CheckCodeForm, RegisterVoteForm, VerifyLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
import json
import uuid
from django.db import connections
from django.contrib.auth.hashers import make_password, check_password as password_check
from django.contrib import messages
import requests
import datetime
import sys


def public_homepage(request):
	return render(request, 'voter_interface/pages/homepage.html', {"title": "Homepage", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ]})


def public_homepage(request):
	return render(request, 'voter_interface/pages/homepage.html', {"title": "Homepage", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ]})



def RegisterSummary(request):
	return render(request, 'voter_interface/pages/voting/register_summary.html', {"title": "Register to Vote Online - Summary", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ],'destination':request.GET.get('destination') })


def RegisterVoterId(request):
	#TODO check if voter is logged in via verify and redirect if not.

	if request.method == "POST":
		verify_username = request.session['verify_username']
		try:
			user = Verify.objects.get(voter_id = request.POST.get('voter_id'),email = verify_username)	
		except:
			messages.error(request, "The voter id you entered does not match the GOV.UK Verify account you are using.")
			return render(request, 'voter_interface/pages/voting/register_voter_id.html', {"title": "Register to Vote Online - Enter Voter Id", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] })

		if user is not None:
			request.session['voter_id_check_passed'] = True
			return redirect('register_election_select')
		else:
			messages.error(request, "The voter id you entered does not match the GOV.UK Verify account you are using.")
			return render(request, 'voter_interface/pages/voting/register_voter_id.html', {"title": "Register to Vote Online - Enter Voter Id", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] })

	else:
		return render(request, 'voter_interface/pages/voting/register_voter_id.html', {"title": "Register to Vote Online - Enter Voter Id", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] })


def RegisterElectionSelect(request):
	#TODO check if the user has passed the voter_id check.
	user = Verify.objects.get(email = request.session['verify_username'])

	elections = GetAvailableElectionsForUser(user.voter_id)
	print(elections)

	return render(request, 'voter_interface/pages/voting/register_election_select.html', {"title": "Register to Vote Online - Select Election", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'], 'elections':elections })


def RegisterPasswordCreation(request):
	if request.method == "POST":
		verify_username = request.session['verify_username']
		user = Verify.objects.get(email = verify_username)	
		#TODO check if voter id check has been passed ..... request.session['voter_id_check_passed'] == True
		#TODO check if the passwords match 
		if user is not None:
			VoterAuth.objects.create(password_hash=make_password(request.POST.get('password')), voter_id=user.voter_id,election_id=request.POST.get('election_id'))

			election_id = request.GET.get('election_id')
			election = Election.objects.get(id = election_id)

			person = Voter.objects.get(voter_id = user.voter_id)

			region_name = PostcodeToRegion(person.address_postcode,election.regions_type)
			region = Region.objects.get(name = region_name)
			
			voter_code = VoterCode.generate_voter_code()
			print("Voter Code: (for testing only, remove once testing complete)")
			print(voter_code) #Delete these print statements once testing is complete
			entry = VoterCode(voter_id= user.voter_id, code=voter_code, election = election, region = region)
			entry.save()

			return redirect('register_complete')
		else:
			messages.error(request, "Something went wrong while registering. Please try again") #TODO improve error handling
			return redirect('register_summary')

	else:
		election_id = request.GET.get('election_id')
		election = Election.objects.get(id = election_id)
		return render(request, 'voter_interface/pages/voting/register_create_password.html', {"title": "Register to Vote Online - Create Password", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] , "election": election })


def RegisterComplete(request):
	#election_name = request.POST.get('election_name')
	election_name = ""
	return render(request, 'voter_interface/pages/voting/register_complete.html', {"title": "Register to Vote Online - Complete", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ], "election_name": election_name })
	

def public_verify(request):
	if request.method == "POST":
		form = VerifyLoginForm(request.POST)
		if form.is_valid():
			
			try:
				destination = request.GET.get('destination')
				user = Verify.objects.get(email = request.POST.get('email'))
				if user is not None:
					# WE NEED TO REMOVE THIS SESSION AFTER TIME and WE NEED TO OFFER LOGOUT
					if  password_check(request.POST.get('password'),user.password_hash):
						request.session['verify_username'] = user.email
						request.session['verify_voter_id'] = user.voter_id
						request.session['verify_forename'] = user.first_name.capitalize()
						request.session['verify_surname'] = user.last_name.capitalize()
						messages.success(request, "Welcome! You have been successfully logged in!")
						return redirect (destination)
					else:
						messages.error(request, "Your credentials does not match our records.")
						form = VerifyLoginForm()
						return render(request, 'voter_interface/pages/verify.html',{'title': "GOV Verify Login", 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify'))], 'welcome': "Verify Login", 'form': form, "destination":destination})
			except Verify.DoesNotExist:
					messages.error(request, "Your credentials does not match our records.")
					form = VerifyLoginForm()
					return render(request, 'voter_interface/pages/verify.html',{'title': "GOV Verify Login", 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify'))], 'welcome': "Verify Login", 'form': form})
		#COPIED CODE HAD NO 'ELSE' HERE - WHAT DO WE WANT TO DO

	else:
		form = VerifyLoginForm()
		destination = request.GET.get('destination')
		return render(request, 'voter_interface/pages/verify.html',{'title': "GOV Verify Login", 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify'))], 'welcome': "Verify Login", 'form': form, "destination":destination})


#CAST VOTE
def CastVoteSummary(request):
	return render(request, 'voter_interface/pages/voting/cast_vote_summary.html', {"title": "Cast Your Vote - Summary", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')) ],'destination':request.GET.get('destination') })


def CastVoteId(request):
	#TODO check if voter is logged in via verify and redirect if not. 
	if request.method == "POST":
		verify_username = request.session['verify_username']
		try:
			user = Verify.objects.get(voter_id = request.POST.get('voter_id'),email = verify_username)	
			if user is not None:
				request.session['voter_id_check_passed'] = True
				return redirect('cast_election_select')
			else:
				messages.error(request, "The voter id you entered does not match the GOV.UK Verify account you are using.")
				return render(request, 'voter_interface/pages/voting/cast_vote_id.html', {"title": "Cast Vote Online - Enter Voter Id", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] })
		except Verify.DoesNotExist:
			messages.error(request, 'Voter does not exists.')
			return redirect('cast_vote_id')
	else:
		return render(request, 'voter_interface/pages/voting/cast_vote_id.html', {"title": "Cast to Vote Online - Enter Voter Id", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] })


def CastElectionSelect(request):
	#TODO check if the user has passed the voter_id check.
	user = Verify.objects.get(email = request.session['verify_username'])

	elections = GetAvailableElectionsForUser(user.voter_id, False)

	return render(request, 'voter_interface/pages/voting/cast_election_select.html', {"title": "Cast Vote Online - Select Election", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name': request.session['verify_surname'], 'elections':elections })


def CastEnterPassword(request):
	#TODO check if the required previous steps have been taken to get here
	if request.method == "POST":
		verify_username = request.session['verify_username']
		user = Verify.objects.get(email = verify_username)	
		#TODO check if voter id check has been passed ..... request.session['voter_id_check_passed'] == True
		#TODO check if the passwords match 
		if user is not None:
			election_id = request.GET.get('election_id')
			request.session['election_id'] = election_id
			if(password_check(request.POST.get('password'), VoterAuth.objects.get(voter_id=user.voter_id,election_id= election_id).password_hash)):
				return redirect('public_vote__ballot')
			else:
				messages.error(request, "The password you entered did not match the one you registered for this election") 
				election = Election.objects.get(id = election_id)
				return render(request, 'voter_interface/pages/voting/cast_enter_password.html', {"title": "Cast Vote Online - Enter Password", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] , "election": election })

		else:
			messages.error(request, "Something went wrong while registering. Please try again") #TODO improve error handling
			return redirect('cast_summary')

	else:
		election_id = request.GET.get('election_id')
		election = Election.objects.get(id = election_id)
		return render(request, 'voter_interface/pages/voting/cast_enter_password.html', {"title": "Cast Vote Online - Enter Password", "breadcrumb": [ ('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Summary', reverse('register_summary')) ], 'first_name':request.session['verify_forename'], 'last_name':request.session['verify_surname'] , "election": election })




def public_vote_home(request):

	return render(request, 'voter_interface/pages/voting/home.html', {"title": "Election Homepage","header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home') )]})


def public_vote_ballot(request): #TODO rename cast_check_code
	if request.method == "POST":
		form = CheckCodeForm(request.POST)
		code = form.data['code']
		voter_id = request.session['verify_voter_id'] 
		try:

			#id should be changed to voter_id - the query - when it exists
			if code in VoterCode.objects.filter(voter_id= voter_id, election_id = request.session['election_id']).values_list('code',flat=True) :
				print("Goes here try")
			
				request.session['code_input'] = code
				return redirect('public_vote__acknowledgement')
			else:

				messages.error(request, "Voter code does not exists or you are not registered with it. Please try again") #TODO improve error handling
				return redirect('public_vote__ballot')	
		except VoterCode.DoesNotExist:
			# error message should be added here
			messages.error(request, "Voter code does not exists or you are not registered with it. Please try again") #TODO improve error handling
			return redirect('public_vote__ballot')	
	else:
		form = CheckCodeForm()
		return render(request, 'voter_interface/pages/voting/cast_check_code.html', {'form': form, "title": "Election Ballot", "header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Home', reverse('public_vote__ballot'))]})

def public_vote_ballot_acknowledgement(request):
	return render(request, 'voter_interface/pages/voting/acknowledgement.html', {"title": "Election Ballot", "header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Home', reverse('public_vote__ballot'))]})



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
	try:
		cursor = connections[region_db_name].cursor()
	except:
		print("WARNING A database does not yet exist for this region.") #This is only in place while the infrastruvture is not set up for all regional databses. 
		return None	
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
		total_ranks = 0
		for key,rank in voter_dict.items():
			new_vote = RegionVote()
			new_vote.election_id = election_id
			new_vote.candidate_id = key
			new_vote.ballot_id = ballot_id
			new_vote.rank = rank
			if rank is not None:
				total_ranks += 1
				SecureVoteToDatabse(new_vote,region_id)
		
		if total_ranks > 0:
			return render(request, 'voter_interface/pages/voting/place.html', {"title": "Election Ballot", "placed": True, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Home', reverse('public_vote__ballot'))]})
		else:
			messages.error(request, "Please choose at least one option.")
			return redirect('public_vote__place_vote');
	else:

		# test data TODO: get this from DB
		checked_code = request.session['code_input']
		#request.session['checked_code'] = ''

		election_id = VoterCode.objects.get(code= checked_code).election_id
		election = Election.objects.get(id = election_id)
		
		election_vote_method = election.election_method
		
		region_id = VoterCode.objects.get(code= checked_code).region_id
		print(region_id)
		candidates = Candidate.objects.filter(region_id = region_id)
		print(candidates[0].first_name)
		#[(1,"1first","1last","4 why address road, Pointless Town, AB1 2CD","Labour"),(2,"2first","2last","4 why address road, Pointless Town, AB1 2CD","Labour")]

		if(election_vote_method == "fptp"):
			return render(request, 'voter_interface/pages/voting/place.html', {"election_id":election_id,"region_id":region_id,"candidates":candidates, "title": "Election Ballot", "header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Ballot', reverse('public_vote__ballot')), ('Place Vote', reverse('public_vote__place_vote')) ]})
		
		elif(election_vote_method == "stv"):
			return render(request, 'voter_interface/pages/voting/place-STV.html', {"election_id":election_id,"region_id":region_id,"candidates":candidates,"title": "Election Ballot", "header_messages": {"welcome": "Welcome to Online Voting", "voter": "Here you will be able to cast your vote in the election by entering your details and online code, or request a code so you can access the ballot"}, 'breadcrumb': [('Home', "http://www.gov.uk"), ('Elections', reverse('public_homepage')), ('Log In', reverse('public_verify')), ('Election Home', reverse('public_vote__home')), ('Election Ballot', reverse('public_vote__ballot')), ('Place Vote', reverse('public_vote__place_vote')) ]})
		
		else:
			messages.error(request, 'An error occured')
			return redirect('public_vote__place_vote')



# This should not be allowed to be accessed in any other way than from check_password (POST)
# when it's working
def check_code(request): #Depreciated
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


def check_password(request): #This function names conflicts with the function written to check passwords #DEPRICATED
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
def cast_vote(request): #DEPRICATED
	return render(request, 'voter_interface/cast_vote.html')

def CastVote(request): #DEPRICATED
	#TO DO
	# - pass election details
	# - validate request 
	# 	- logged in
	#	- verify
	#	- voter password
	#	- voter code
	# - switch template based on voting system. 

	return render(request, 'voter_interface/ballot_paper_fptp.html')


def register_to_vote(request): #DEPRICATRED
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
	api_url = 'https://api.postcodes.io/postcodes/{0}'
	postcode_json = requests.get(url=api_url.format(post_code)).json()
	if(region_type in postcode_json["result"]):
		return postcode_json["result"][region_type]
	else:
		return None


def GetAvailableElectionsForUser(voter_id,registering=True):
	#Get Voters Regions
	voter = Voter.objects.get(voter_id= voter_id)
	region_name_list = []
	check_region_types = ["parliamentary_constituency", "admin_district"] # TODO add other region types e.g. local

	for region_type in check_region_types:
		region_name_list.append( PostcodeToRegion(voter.address_postcode.replace(" ",""),region_type) )

	#Get all registration open elections for those regions
	#Aberconwy

	elections = []
	print(region_name_list)
	if(registering):
		for region_name in region_name_list:
			if(not region_name == None):
				try:
					region = Region.objects.get(name = region_name)
					print(region)
					
					if(not region == None):
						# date checking
						for election in Election.objects.filter(regions__in=[region], end_date__gte = datetime.date.today(), start_date__lte = datetime.date.today()):
							# check if voter registered for the election
							if not VoterCode.objects.filter(voter_id = voter_id, election_id = election.id).exists():
								elections.append(election)
				except:
					e = sys.exc_info()[0]
					print(e)
					print("Region not found, likely a non created admin_district")
	else:
		for region_name in region_name_list:
			if(not region_name == None):
				try:
					region = Region.objects.get(name = region_name)
					
					if(not region == None):
						open_elections = Election.objects.filter(regions__in=[region], end_date__gte = datetime.date.today(), start_date__lte = datetime.date.today())
						for election in open_elections:
							if(VoterAuth.objects.filter(election_id=election.id,voter_id = voter_id).count() > 0):
								elections.append(election)
				except:
					print("Region not found, likely a non created admin_district")

	return elections


#REMOVE - ONLY FOR TESTING #TODO remove this section once testing is finished

#GOV.UK Verify Details for A Fiction:
#afiction@gmail.com
#GROUP2

#Voter id:
#I3GJ2ZDUMTHT9T9

#Detils for john doe:
#doej@gmail.com
#GROUP2
#Voter ID: K2GJ1ZPUNTLT8K9

def DeleteAFictionPasswords(request):
	VoterAuth.objects.filter(voter_id="I3GJ2ZDUMTHT9T9").delete()
	VoterCode.objects.filter(voter_id="I3GJ2ZDUMTHT9T9").delete()

	messages.error(request, "A Fiction's passwords for elections deleted.") 
	return redirect('register_summary')
	
	
def DeleteJohnPasswords(request):
	VoterAuth.objects.filter(voter_id="K2GJ1ZPUNTLT8K9").delete()
	VoterCode.objects.filter(voter_id="K2GJ1ZPUNTLT8K9").delete()

	messages.error(request, "Johns's passwords for elections deleted.") 
	return redirect('register_summary')
	
