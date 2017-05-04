from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from voting_system.models import *
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password as admin_password_check
from voting_system.forms import *
from voting_system.views.CheckAuthorisation import CheckAuthorisation, GetUserRoles
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.conf import settings
from random import choice
from random import randint
import datetime
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db import connections

from voting_system.views.voter_interface import PostcodeToRegion
def admin_master_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[])
	if(authorised):
		return render(request, 'admin_interface/pages/index.html', {'title': "Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home')], 'first_name': request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})
	else:
		return redirect('admin_login')


# ---- Authentication START ---- #
def admin_login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			try:
				user = Admin.objects.get(user_name = request.POST.get('username'))
				if user is not None:
					#remove this check SAM ADD encryption ;P
					if admin_password_check(request.POST.get('password'),user.password_hash):
						request.session['username'] = user.user_name
						request.session['forename'] = user.first_name.capitalize()
						messages.success(request, "Welcome! You have been successfully logged in!")
						return redirect ('admin_master_homepage')

					else:
						form = LoginForm()
						messages.error(request, "Your credentials does not match our records.")
						return render(request, 'admin_interface/pages/authentication/login.html',{'title': "Login",'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ('Login', reverse('admin_login'), 'lock')], 'form': form, 'welcome': "Admin Login"})
			except Admin.DoesNotExist:
				form = LoginForm()
				messages.error(request, "Your credentials does not match our records.")
				return render(request, 'admin_interface/pages/authentication/login.html',{ 'title': "Login",'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ('Login', reverse('admin_login'), 'lock')], 'form': form})
	else:
		form = LoginForm()
		return render(request, 'admin_interface/pages/authentication/login.html',{'title': "Login", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ('Login', reverse('admin_login'), 'lock')], 'welcome': "Admin Login", 'form': form})


def admin_logout(request):
	try:
		del request.session['username']
		del request.session['forename']
	except:
		pass
	
	messages.success(request, "You have been successfully logged out")
	return redirect ('public_homepage')

# ---- Authentication END ---- #

# ---- Admin START ---- #


def admin_view(request, page_id=1): #list of all admins
	authorised,username = CheckAuthorisation(request,True,[('admin__view',)])
	if(authorised):
		admin_list = Admin.objects.all().order_by('id')
		paginator = Paginator(admin_list, settings.PAGINATION_LENGTH)
		try:
			admins = paginator.page(page_id)
		except PageNotAnInteger:
			admins = paginator.page(1)
		except EmptyPage:
			admins = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/admin/view.html', {'title': "View Admins", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Admin Homepage", reverse('admin_homepage'), 'user'), ('View',  reverse('admin_view'), 'list')],  'first_name':request.session['forename'], 'admins': admins, "roles": GetUserRoles(request.session.get('username'))})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_homepage')


def admins_homepage(request): #page with link to admin list and creating an admin (maybe this page isn't required??)
	authorised,username = CheckAuthorisation(request,True,[('admin',)])
	if(authorised):
		print(GetUserRoles(request.session.get('username')))
		return render(request, 'admin_interface/pages/admin/index.html', {'title': 'Admin Homepage','breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Admin Homepage", reverse('admin_homepage'), 'user')], 'first_name': request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})
	else:
		return redirect('admin_login')


def admin_edit(request, id =None): #editing a specific admin
	authorised,username = CheckAuthorisation(request,True,[('admin__edit',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_homepage')
	else:
		admin_init = get_object_or_404(Admin, id=id)
		role_current = AdminRole.objects.filter(admin_id = id).values_list("role_id", flat=True)
		roles = Role.objects.all()

		if request.method == "POST":

			form = AdminForm(request.POST, instance=admin_init)
			if form.is_valid():
				admin = form.save(commit=False)
				selected_roles = request.POST.getlist('roles[]')
				if 'current_password' in request.POST:
					if admin_password_check(request.POST.get('current_password'), admin_init.password_hash):
						if 'password' not in request.POST:
							messages.error(request, "New password field is empty.")
							return render(request, 'admin_interface/pages/admin/form.html', {'form': form, 'title': "Edit Admin", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Admin Homepage", reverse('admin_homepage'), 'user'), ("Edit Admin", reverse('admin_edit', kwargs={'id':id}), 'pencil')], 'roles': roles, 'current_roles': role_current,  'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})
						else:

							if(request.POST.get('password') != request.POST.get('repeatPassword')):
								messages.error(request, "Password Does not match")
								return render(request, 'admin_interface/pages/admin/form.html', {'form': form, 'roles': roles}) 
							else:
								admin.password_hash =  make_password(request.POST.get('password'))
							 
					else:
						messages.error(request, "Current Password Does not match our records")
						return render(request, 'admin_interface/pages/admin/form.html', {'form': form, 'title': "Edit Admin", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Admin Homepage", reverse('admin_homepage'), 'user'), ("Edit Admin", reverse('admin_edit', kwargs={'id':id}), 'pencil')], 'roles': roles, 'current_roles': role_current,  'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})
				
				admin.save()
				# Dirty way... 
				# Remove all previous roles for admin then assign new ones -- TALK TO ME ABOUT THIS -- need a more efficienet way  
				AdminRole.objects.filter(admin_id = id).delete()
				
				for role in selected_roles:
					new_role = AdminRole()
					new_role.id = getNextID("admin_roles")
					new_role.admin_id = id
					new_role.role_id = role
					new_role.save()

				
				messages.success(request, "Sucessfully changed!")
				return redirect('admin_view')
		else:
			form = AdminForm(instance=admin_init)
			
		return render(request, 'admin_interface/pages/admin/form.html', {'form': form, 'title': "Admin Edit" , 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Admin Homepage", reverse('admin_homepage'), 'user'), ("Edit Admin", reverse('admin_edit', kwargs={'id':id}), 'pencil')], 'roles': roles, 'current_roles': role_current,  'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})


def admin_create(request):#creates an admin
	authorised,username = CheckAuthorisation(request,True,[('admin__create',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_homepage')
	else:
		roles = Role.objects.all()
		if request.method == "POST":
			form = AdminForm(request.POST)
			if form.is_valid():
				if(request.POST.get('password') != request.POST.get('repeatPassword')):
					return render(request, 'admin_interface/pages/admin/form.html', {'title': 'Create new Admin', 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Admin Homepage", reverse('admin_homepage'), 'user'), ("Create new Admin", reverse('admin_create'), 'plus')],'form': form, 'roles': roles, 'errors': ["Password Does not match"]})
				else:
					id = getNextID("admins")
					admin = form.save(commit=False)
					admin.id = id
					admin.password_hash = make_password(request.POST.get('password'))
					admin.save()
					selected_roles = request.POST.getlist('roles[]')

					for role in selected_roles:
						new_role = AdminRole()
						new_role.id = getNextID("admin_roles")
						new_role.admin_id = id
						new_role.role_id = role
						new_role.save()
				
					return redirect('admin_view')
		else:
			form = AdminForm()
			
			return render(request, 'admin_interface/pages/admin/form.html', {'title': 'Create new Admin', 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Admin Homepage", reverse('admin_homepage'), 'user'), ("Create new Admin", reverse('admin_create'), 'plus')], 'first_name': request.session['forename'], 'form': form, 'roles': roles})


def admin_delete(request, id=None):#deletes a specific admin
	authorised,username = CheckAuthorisation(request,True,[('admin__delete',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_homepage')
	else:
		admin = get_object_or_404(Admin, id=id)
		admin.delete()
		messages.error(request, "Admin #"+id+" has been deleted!")
		return redirect('admin_view')


# ---- Admin END ---- #

# ---- Voter Code START ---- #


def voter_code_homepage(request): #not sure we need these home pages??
	authorised,username = CheckAuthorisation(request,True,[('voter_codes__view',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:
		return render(request, 'admin_interface/pages/codes/index.html', {'title': "Voter Code Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Voter Codes Homepage", reverse('voter_code_homepage'), 'address-card')], 'first_name': request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})


def voter_code_view(request, page_id=1, id=None, election_id=None, sort=None):
	authorised,username = CheckAuthorisation(request,True,[('voter_codes__view',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('voter_code_homepage')
	else:
		authorised,username = CheckAuthorisation(request,True,[("voter_codes__view",)])
		if(authorised):
			election = election_id
			sort = sort
			if election_id != None:
				if sort != None:
					codes = VoterCode.objects.all().filter(election_id=election_id).order_by(sort)
				else:
					codes = VoterCode.objects.all().filter(election_id=election_id)
			elif id != None:
				codes = VoterCode.objects.all().filter(id = id)	
			else:
				if sort != None:
					codes = VoterCode.objects.all().order_by(sort)
				else:
					codes = VoterCode.objects.all()
			paginator = Paginator(codes, settings.PAGINATION_LENGTH)
			try:
				voter_codes = paginator.page(page_id)
			except PageNotAnInteger:
				voter_codes = paginator.page(1)
			except EmptyPage:
				voter_codes = paginator.page(paginator.num_pages)
			return render(request, 'admin_interface/pages/codes/view.html', {'title': "View Voter Codes", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Voter Codes Homepage", reverse('voter_code_homepage'), 'address-card'), ("View Voter Codes", reverse('voter_code_view'), 'list')], 'first_name':request.session['forename'], 'voter_codes': voter_codes,  "election": election,"sort": sort})
		else:
			messages.error(request, "Access Denied. You do not have sufficient privileges.")
			return redirect('voter_code_homepage')

def voter_code_create_rand(request):

	for i in range(0, 30):
		code = VoterCode()
		code.id = getNextID("voter_codes")
		code.election_id = randint(16, 23)
		code.voter_id = randint(1000, 88888)
		code.sent_status = choice([True, False])
		code.verified_date = get_random_date(2016)
		code.invalidated_date = get_random_date(2017)
		code.save()

	return render(request, 'admin_interface/pages/codes/index.html')

def voter_code_print_unissued(request):
	authorised,username = CheckAuthorisation(request,True,[('voter_codes__print',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('voter_code_homepage')
	else:
		if request.POST:
			election = request.POST.get('elections')
			data = {"data": []}
			try:

				election_details = Election.objects.values().filter(id=election)
				
				# Get all voter codes where not be printed
				try:
					voter_ids = VoterCode.objects.filter(election_id = election).filter(sent_status = False).filter(Q(invalidated_date__isnull = True) | Q(invalidated_date__gte = datetime.date.today())).values('voter_id', 'code')
					print(voter_ids)
					for id in voter_ids:
						print(id)
						try:
							details = Voter.objects.filter(voter_id = id['voter_id']).values()
						

							data['data'].append({"election": election_details[0], "voter": details[0], "code": id['code'], "region": PostcodeToRegion(details[0]['address_postcode']) })

						except Voter.DoesNotExist:
							messages.error(request, "One or more voters does not exists. Please try again.")
							redirect('voter_code_print_unissued')

				except VoterCode.DoesNotExist:
					messages.error(request, "One or more voter codes does not exist.")
					return redirect('voter_code_print_unissued')
				
			except Election.DoesNotExist:
				messages.error(request, "One or more elections does not exist.")
				return redirect('voter_code_print_unissued')
			pdf = render_to_pdf('admin_interface/pages/codes/print/letter.html', data)
			
			if pdf:
				response = HttpResponse(pdf, content_type='application/pdf')
				filename = "Unissued_codes_%s.pdf" %(election)
				content = "print; filename="+filename
				download = request.GET.get("download")
				if download:
					content = "print; filename="+filename
				response['Content-Disposition'] = content
				return response
			messages.error
			return redirect("voter_code_print")
		
		else:
			elecs = Election.objects.filter(Q(voting_end_date__gte = datetime.date.today()))
			elections = []

			for elec in elecs:
				if VoterCode.objects.all().filter(election_id=elec.id).filter(sent_status = False).filter( Q(invalidated_date__isnull = True) | Q(invalidated_date__gte = datetime.date.today())).exists():
					elections.append(elec)
			
			return render(request, 'admin_interface/pages/codes/unissued.html', {'title': 'Print Unissued voter codes', 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Voter Codes Homepage", reverse('voter_code_homepage'), 'address-card'), ("Print Unissued", reverse('voter_code_print_unissued'))], 'first_name': request.session['forename'], "elections": elections, "roles": GetUserRoles(request.session.get('username'))})


	return True



def voter_code_populate(request):
	authorised,username = CheckAuthorisation(request,True,[('voter_codes',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('voter_code_homepage')
	else:
		if request.method == "POST":
			form = VoterCodeForm(request.POST)
			if form.is_valid():
				election = form.instance.election
				form.save(commit=False)
				print(election)
				VoterCode.populate_voter_codes(election)
				messages.success(request, "Successfully added voter codes for "+ election.name)
				return redirect('voter_code_populate')
		else:
			form = VoterCodeForm()
		return render(request, 'admin_interface/pages/codes/form.html', {"title": "Populate Voter Codes", 'breadcrumb': [("Home", reverse('voter_code_homepage'), 'address-card'), ("Populate Voter Codes", reverse('voter_code_populate'))], 'first_name':request.session['forename'], 'form': form})
		# ---- Voter Code END ---- #
	
# ---- MISC START (TO SORTT) ---- #

# ---- Candidates START ---- #


def candidate_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('candidates',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:
		return render(request, 'admin_interface/pages/candidates/index.html', {"title": "Candidates Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Candidate Homepage", reverse('candidate_homepage'), 'user')], 'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})


def candidate_view(request, page_id=1):
	authorised,username = CheckAuthorisation(request,True,[('candidates__view',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('candidate_homepage')
	else:
		candidate_list = Candidate.objects.all().order_by('id')
		paginator = Paginator(candidate_list, settings.PAGINATION_LENGTH)
		try:
			candidates = paginator.page(page_id)
		except PageNotAnInteger:
			candidates = paginator.page(1)
		except EmptyPage:
			candidates = paginator.page(paginator.num_pages)
		
		return render(request, 'admin_interface/pages/candidates/view.html', {'title': "View Candidates", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Candidate Homepage", reverse('candidate_homepage'), 'user'), ("View Candidates", reverse('candidate_view'), 'list')], 'candidates':candidates,  'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})


def candidate_create(request):
	authorised,username = CheckAuthorisation(request,True,[('candidates__create',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('candidate_homepage')
	else:
		if request.method == "POST":
			
			form = CandidateForm(request.POST)
			party = request.POST.get('party_id')
			region = request.POST.get('region_id')
			if form.is_valid():

				candidate = form.save(commit=False)
				candidate.id = getNextID('candidates')
				candidate.party_id = party
				candidate.region_id = region
				candidate.save()
				messages.success(request, "Successfully added a new candidiate!")
			return redirect('candidate_view')
		else:
			regions = Region.objects.all()
			form = CandidateForm()
			return render(request, 'admin_interface/pages/candidates/form.html', {"title": "Create Candidate", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Candidate Homepage", reverse('candidate_homepage'), 'user'), ("Create new Candidate", reverse('candidate_create'), 'plus')],  'first_name':request.session['forename'], 'form': form, 'regions': regions, "roles": GetUserRoles(request.session.get('username')) })


def candidate_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[('candidates__edit',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('candidate_homepage')
	else:			
		candidate = get_object_or_404(Candidate, id=id)
		if request.method == "POST":
			form = CandidateForm(request.POST, instance=candidate)
			party = request.POST.get('party_id')
			region = request.POST.get('region_id')
			if form.is_valid():
				candidate = form.save(commit=False)
				candidate.party_id = party
				candidate.region_id = region
				candidate.save()
				messages.success(request, "Candidate #"+id+" successfully update!")
				return redirect('candidate_view')
		else:
			
			form = CandidateForm(instance=candidate)
			form.fields['party_id'].initial = candidate.party_id
			form.fields['region_id'].initial = candidate.region_id

		return render(request, 'admin_interface/pages/candidates/form.html', { "title": "Edit Candidate", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Candidate Homepage", reverse('candidate_homepage'), 'user'), ("Edit Candidate", reverse('candidate_edit',kwargs={'id':id}), 'pencil')], 'first_name':request.session['forename'], 'form': form
		, "roles": GetUserRoles(request.session.get('username'))})


def candidate_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[('candidates__delete',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('candidate_homepage')
	else:		
		candidate = get_object_or_404(Candidate, id=id)
		candidate.delete()
		messages.error(request, "Candidate #"+id+" has been deleted!")
		return redirect('candidate_view')


# ---- Candidates END ---- #

# ---- Election START ---- #


def election_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('elections',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:		
		elections = Election.objects.all()
		return render(request, 'admin_interface/pages/elections/index.html', {"title": 'Election Homepage', 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Election Homepage", reverse('election_homepage'), 'file-text-o')],'first_name':request.session['forename'], 'elections': elections, "roles": GetUserRoles(request.session.get('username')) })
	

def election_view(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[('elections__view',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')
	else:		
		election_list = Election.objects.all().order_by('id')
		paginator = Paginator(election_list, settings.PAGINATION_LENGTH)
		try:
			elections = paginator.page(page_id)
		except PageNotAnInteger:
			elections = paginator.page(1)
		except EmptyPage:
			elections = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/elections/view.html', {'title': "View Elections", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Election Homepage", reverse('election_homepage'), 'file-text-o'), ("View Elections", reverse('election_view'), 'list')],'first_name':request.session['forename'], 'elections': elections, "roles": GetUserRoles(request.session.get('username'))})
	

def election_create(request):
	authorised,username = CheckAuthorisation(request,True,[('elections__create',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')
	else:		
		candidates = Candidate.objects.all()
		if request.method == "POST":
			form = ElectionForm(request.POST)
			if form.is_valid():
				election_id = getNextID('elections')
				election = form.save(commit=False)
				election.id = election_id
				election.save()
				
				#list of party_ids
				party_ids = []
				# Add Candidates
				selected_candidates = request.POST.getlist('candidates[]')
				for candidate in selected_candidates:
					new_candidate = ElectionCandidate()
					new_candidate.id = getNextID("election_candidates")
					new_candidate.election_id = election_id
					new_candidate.candidate_id = candidate
					new_candidate.save()
					
					candidate_data = Candidate.objects.get(id = candidate)
					if candidate_data.party_id not in party_ids:
						party_ids.append(candidate_data.party_id)

				# Add parties
				
				for party in party_ids:
					new_party = ElectionParty()
					new_party.id = getNextID("election_parties")
					new_party.election_id = election_id
					new_party.party_id = party
					new_party.save()
				
				# Add parties
				selected_regions = request.POST.getlist('region_id')
				for region in selected_regions:
					new_region = ElectionRegion()
					new_region.id = getNextID("election_regions")
					new_region.election_id = election_id
					new_region.region_id = region
					new_region.save()

				messages.success(request, "Successfully added new Election!")
				return redirect('election_view')
		else:
			form = ElectionForm()
			regions = Region.objects.all()
	
		return render(request, 'admin_interface/pages/elections/form.html', {'title': 'Create Election', 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Election Homepage", reverse('election_homepage'), 'file-text-o'), ("Create new Election", reverse('election_create'), 'plus')],'first_name': request.session['forename'], 'form': form, 'regions': regions,'candidates': candidates, "roles": GetUserRoles(request.session.get('username'))})


def election_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[('elections__edit',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')
	else:
		election = get_object_or_404(Election, id=id)
		candidates_current = ElectionCandidate.objects.filter(election_id = id).values_list("candidate_id", flat=True)
		region_current = ElectionRegion.objects.filter(election_id = id).values_list("region_id", flat=True)
		
		if request.method == "POST":
			form = ElectionForm(request.POST, instance=election)

			if form.is_valid():


				election = form.save(commit=False)
				election.save()

				'''#check if th

				party_ids = []
				party_ids_remove = []
				# Add Candidates
				selected_candidates = request.POST.getlist('candidates[]')
				print(candidates_current)
				cur_cand = ElectionCandidate.objects.filter(election_id = id).values_list("candidate_id", flat=True)
				for candidate in selected_candidates:
					#check if this candidate is in current
					if candidate not in cur_cand:
						new_candidate = ElectionCandidate()
						new_candidate.id = getNextID("election_candidates")
						new_candidate.election_id = id
						new_candidate.candidate_id = candidate
						new_candidate.save()

					
						candidate_data = Candidate.objects.get(id = candidate)
						if candidate_data.party_id not in party_ids:
							party_ids.append(candidate_data.party_id)
					else:
						del candidates_current[candidate]
				
				
				for cur in cur_cand:
					#delete any candidates which not be reused from previous
					# get party id then append to party_ids_remove
					ElectionCandidate.objects.filter(candidate_id = cur).delete()
				
				
				for party in party_ids:
					new_party = ElectionParty()
					new_party.id = getNextID("election_parties")
					new_party.election_id = id
					new_party.party_id = party
					new_party.save()

				for party in party_ids_remove:
					#remove any not used
					ElectionParties.objects.filter(party_id = party).delete()
				# Add parties
				selected_regions = request.POST.getlist('region_id')
				for region in selected_regions:
					if region not in region_current:
						new_region = ElectionRegion()
						new_region.id = getNextID("election_regions")
						new_region.election_id = id
						new_region.region_id = region
						new_region.save()
					else:
						regions_current.pop(region)
				for cur in region_current:
					#delete any regions which not be reused from previous
					ElectionRegion.objects.filter(region_id = cur).delete()'''
				messages.success(request, candidates_current)
				return redirect('election_view')
		else:
			form = ElectionForm(instance=election)
		candidates = Candidate.objects.all()
		regions = Region.objects.all()
		return render(request, 'admin_interface/pages/elections/form.html', {'title': 'Edit Election', 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Election Homepage", reverse('election_homepage'), 'file-text-o'), ("Edit Election", reverse('election_edit',kwargs={'id':id}), 'pencil')],'first_name': request.session['forename'], 'form': form, 'regions': regions,'candidates': candidates, 'current_candidates': candidates_current,'current_regions':region_current , "roles": GetUserRoles(request.session.get('username'))})


def election_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[('elections__delete',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')
	else:		
		election = get_object_or_404(Election, id=id)
		election.delete()
		messages.error(request, "Election #"+id+" has been Deleted")
		return redirect('election_view')
	
# ---- Election END ---- #

# ---- Role START ---- #


def role_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('roles',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:		
		return render(request, 'admin_interface/pages/roles/index.html', {'title': "Roles Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks')], 'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username')) })


def role_view(request, page_id=1):
	authorised,username = CheckAuthorisation(request,True,[('role__view',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_homepage')
	else:
		roles_list = Role.objects.all().order_by('id')
		paginator = Paginator(roles_list, settings.PAGINATION_LENGTH)
		try:
			roles = paginator.page(page_id)
		except PageNotAnInteger:
			roles = paginator.page(1)
		except EmptyPage:
			roles = paginator.page(paginator.num_pages)
		
		return render(request, 'admin_interface/pages/roles/view.html', {'title': "View Roles", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks'), ("View Role", reverse('role_view'), 'list')], 'first_name':request.session['forename'], 'roles': roles, "adminRoles": GetUserRoles(request.session.get('username'))})
	

def role_create(request):
	authorised,username = CheckAuthorisation(request,True,[('role__create',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_homepage')
	else:
		if request.method == "POST":
			form = RoleForm(request.POST)
			if form.is_valid():
				role = form.save(commit=False)
				role.id = getNextID('roles')
				role.save()
				messages.success(request, "Successfully added 1 new role")
				return redirect('role_view')
		else:
			form = RoleForm()
		return render(request, 'admin_interface/pages/roles/form.html', {'title': "Create new Role",  'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks'), ("Create new Role", reverse('role_create'), 'plus')], 'first_name':request.session['forename'], 'form': form})


def role_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[('role__edit',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_homepage')
	else:
		role = get_object_or_404(Role, id=id)
		if request.method == "POST":
			form = RoleForm(request.POST, instance=role)
			if form.is_valid():
				role = form.save(commit=False)
				role.save()
				messages.success(request, "Role #"+id+" Successfully Updated!")
				return redirect('role_view')
		else:
			form = RoleForm(instance=role)
			return render(request, 'admin_interface/pages/roles/form.html', {'title': "Edit new Role",  'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks'), ("Edit Role", reverse('role_edit', kwargs={'id':id}), 'pencil')], 'first_name':request.session['forename'], 'form': form})
		return render(request, 'admin_interface/pages/roles/form.html', {'title': "Edit new Role",  'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks'), ("Edit Role", reverse('role_edit', kwargs={'id':id}), 'pencil')], 'first_name':request.session['forename'], 'form': form})


def role_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[('role__delete',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_homepage')
	else:
		role = get_object_or_404(Role, id=id)
		role.delete()
		messages.error(request, "Role #"+id+" has been deleted!")
		return redirect('role_view')
	

# ---- Role END ---- #

# ---- Party START--- #


def party_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[("party",)])
	if(authorised):
		return render(request, 'admin_interface/pages/parties/index.html', {'title': "Party Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Parties Homepage", reverse('party_homepage'), 'users')], 'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_master_homepage')


def party_view(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[("party__view",)])
	if(authorised):
		party_list = Party.objects.all().order_by('id')
		paginator = Paginator(party_list, settings.PAGINATION_LENGTH)
		try:
			parties = paginator.page(page_id)
		except PageNotAnInteger:
			parties = paginator.page(1)
		except EmptyPage:
			parties = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/parties/view.html', {'title': "Party Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Parties Homepage", reverse('party_homepage'), 'users'),("View all Parties", reverse('party_view'), 'list')], 'first_name':request.session['forename'], 'parties': parties, "roles": GetUserRoles(request.session.get('username'))})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_homepage')


def party_create(request):
	authorised,username = CheckAuthorisation(request,True,[("party__create",)])
	if(authorised):
		if request.method == "POST":
			form = PartyForm(request.POST)
			if form.is_valid():
				party = form.save(commit=False)
				party.id = getNextID('parties')
				party.save()
				messages.success(request, "Successfully added 1 new party!")
				return redirect('party_view')
		else:
			form = PartyForm()
		return render(request, 'admin_interface/pages/parties/form.html', {'title': "Create new Party", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Parties Homepage", reverse('party_homepage'), 'users'), ("Create new Party", reverse('party_create'), 'plus')], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_homepage')


def party_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("party__delete",)])
	if(authorised):
		party = get_object_or_404(Party, id=id)
		party.delete()
		messages.error(request, "Party #"+id+" has been deleted!")
		return redirect('party_view')
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_homepage')


def party_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("party__edit",)])
	if(authorised):
		party = get_object_or_404(Party, id=id)
		if request.method == "POST":
			form = PartyForm(request.POST, instance=party)
			if form.is_valid():
				party = form.save(commit=False)
				
				party.save()
				messages.success(request, "Party #"+id+" has been modifed!")
				return redirect('party_view')
		else:
			form = PartyForm(instance=party)
		return render(request, 'admin_interface/pages/parties/form.html', {'title': "Create new Party", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Parties Homepage", reverse('party_homepage'), 'users'), ("Edit Party", reverse('party_edit', kwargs={'id':id}), 'pencil')], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_view')

# ---- Party  END--- #

# -----  Region ----- #


def region_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[("region",)])
	if(authorised):
		return render(request, 'admin_interface/pages/regions/index.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Region Homepage", reverse('region_homepage'), 'map-marker')], 'first_name':request.session['forename'], "roles": GetUserRoles(request.session.get('username'))})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_master_homepage')


def region_view(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[("region__view",)])
	if(authorised):
		regions_list = Region.objects.all().order_by('id')
		paginator = Paginator(regions_list, settings.PAGINATION_LENGTH)

		try:
			regions = paginator.page(page_id)
		except PageNotAnInteger:
			regions = paginator.page(1)
		except EmptyPage:
			regions = paginator.page(paginator.num_pages)

		return render(request, 'admin_interface/pages/regions/view.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Region Homepage", reverse('region_homepage'), 'map-marker'), ("View Regions", reverse('region_view'), 'list')], 'first_name':request.session['forename'], 'regions': regions, "roles": GetUserRoles(request.session.get('username'))})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')


def region_create(request):
	authorised,username = CheckAuthorisation(request,True,[("region__create",)])
	if(authorised):
		if request.method == "POST":
			form = RegionForm(request.POST)
			if form.is_valid():
				region = form.save(commit=False)
				region.id = getNextID('regions')
				region.save()
				messages.success(request, "Successfully added a new region!")
				return redirect('region_view')
		else:
			form = RegionForm()
		return render(request, 'admin_interface/pages/regions/form.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Region Homepage", reverse('region_homepage'), 'map-marker'), ("Create new region", reverse('region_create'), 'plus')], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')


def region_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("region__edit",)])
	if(authorised):
		region = get_object_or_404(Region, id=id)
		if request.method == "POST":
			form = RegionForm(request.POST, instance=region)
			if form.is_valid():
				region = form.save(commit=False)
				region.save()
				messages.success(request, 'Region #'+id+' Has been Update')
				return redirect('region_view')
		else:
			form = RegionForm(instance=region)
		return render(request, 'admin_interface/pages/regions/form.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Region Homepage", reverse('region_homepage'), 'map-marker'), ("Edit Region", reverse('region_edit', kwargs={'id': id}), 'pencil')], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')


def region_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("region__delete",)])
	if(authorised):
		region = get_object_or_404(Region, id=id)
		region.delete()
		messages.error(request, "Region #"+id+" successfuly deleted!")
		return redirect('region_view')
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')
# ---- Region END --- #

# ---- Statistics START --- #

def statistics_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[("statistics",)])
	if(authorised):
		if request.POST:
			return redirect('election_demographics', election_id=request.POST.get('election'))
		else:
			elections = Election.objects.filter(Q(voting_end_date__lte = datetime.date.today()))
			print(elections)
			return render(request, 'admin_interface/pages/statistics/index.html', {'title': "Statistics Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Statistics Homepage", reverse('statistics_homepage'))], 'first_name':request.session['forename'], "elections": elections})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_master_homepage')

def Demographics(request,election_id):
	authorised,username = CheckAuthorisation(request,True,[('statistics__demographics',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:
		election = 	get_object_or_404(Election, id=election_id)	
		regions = election.regions.all()

		return render(request, 'admin_interface/pages/statistics/view_demographics.html', {'title': "Election Demographics Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Statistics Homepage", reverse('statistics_homepage')), ("View Statistics", None)], 'first_name':request.session['forename'], "election":election,"regions":regions })

def GetGraph(request,election_id,region_id):

	
	authorised,username = CheckAuthorisation(request,True,[('statistics__demographics',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:
		election = 	get_object_or_404(Election, id=election_id)	
		
		elegible_voters = AllVoters(election_id)
		registered_voters = FilterVotersByRegistered(elegible_voters,election_id)
		
		

		demographic_statistics = []

		elegible_voters_count = len(elegible_voters)
		registered_voters_count = len(registered_voters)

		demographic_statistics.append( MakeGraphInstance('Election Wide Eligible Voters who Registered Online',[['Did not Register Online',elegible_voters_count-registered_voters_count],['Registered Online',registered_voters_count]],0) )

		region = Region.objects.get(id= region_id)
		i = 1

		region_elegible_voters = FilterVotersByRegion(elegible_voters,region.name,election.regions_type)
		elegible_voters_count = len(region_elegible_voters)

		region_registered_voters = FilterVotersByRegistered(region_elegible_voters,election_id)
		registered_voters_count = len(region_registered_voters)

		demographic_statistics.append( MakeGraphInstance(region.name + ': Eligible Voters who Registered Online',[['Did not Register Online',elegible_voters_count-registered_voters_count],['Registered Online',registered_voters_count]],i+1) )


		return render(request, 'admin_interface/pages/statistics/get_graph.html', {'title': "Election Demographics Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Statistics Homepage", reverse('statistics_homepage')), ("Get Graph", None) ], "election":election, "demographic_statistics":demographic_statistics })



# ---- Statistics END --- #



def getNextID(tblName):
	cursor = connection.cursor()
	cursor.execute( "select nextval('"+tblName+"_id_seq')")
	row = cursor.fetchone()
	cursor.close()
	return row[0]

# ---- Misc Functions START --- #
def render_to_pdf(template_src, context_dict={}):
    #get template
    template = get_template(template_src)
    # add dynamic attributes
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return  HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def get_random_date(year):

    # try to get a date
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y')

    # if the value happens to be in the leap year range, try again
    except ValueError:
		

        get_random_date(year)
# ---- Misc Functions END --- #

# don't move these functions or change their names. I am working on them.
# -- okay -- I've changed the region popuate to generated correct ID with sequences - CA
# MOVED populate_voter_codes into the voter code section LINE:


def region_populate(request):
	authorised,username = CheckAuthorisation(request,True,[('region',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')
	else:
		if not Region.objects.all():
			Region.populate_regions()
			messages.success(request, "Regions successfuly populated!")
			return redirect('region_view')
		else :
			messages.error(request, "Regions are already populated.")
			return redirect( 'region_view', { 'first_name': request.session['forename']})



def test_vote_fetch(request):
	election_id = 1
	region_id = 1
	candidate_id = 1

	votes = VoteResults(election_id,region_id,candidate_id)
	
	voters = AllVoters(election_id,region_id)

	return render(request, 'admin_interface/pages/test_fetch_vote.html', {"votes":votes,"voters":voters})


def VoteResults(election_id,region_id):
	#TODO add the filtering
	region_db_name = "region"+str(region_id)
	cursor = connections[region_db_name].cursor()
	cursor.execute("SELECT election_id,candidate_id,ballot_id,rank from votes ;")
	votes = cursor.fetchall()

	if(election_id):
		election_id = int(election_id)
		if(election_id > 0):
			votes = [vote for vote in votes if vote[0] == election_id]
	return votes


def AllVoters(election_id=None,region_id=None):
	cursor = connections["people"].cursor()
	cursor.execute("SELECT voter_id,address_postcode from voters ;")
	voters = cursor.fetchall()
	if(election_id):
		voters = FilterVotersByElection(voters,election_id)

	if(region_id):
		voters = FilterVotersByRegion(voters,region_id)

	return voters

def FixBrokenPostCodes(working_code,broken_code):
	cursor = connections["people"].cursor()
	cursor.execute("UPDATE voters SET address_postcode = '"+working_code+"' WHERE address_postcode = '"+broken_code+"' ;")

def CheckVoters(voters,election_id):
	print("starting check")
	required_fixes = []
	working_code = "AB12 3LP"
	current_code = ""

	election = Election.objects.get(id=election_id)
	region_names = [region.name for region in election.regions.all()]
		
	for voter in voters:
		current_code = voter[1]
		try:

			voter_region = PostcodeToRegion(voter[1],election.regions_type)
			working_code = voter[1]
		except:
			print(current_code)
			required_fixes.append( (working_code,current_code) )
	
	for fix in required_fixes:
		#print(fix)
		FixBrokenPostCodes(fix[0],fix[1])

def FilterVotersByElection(voters,election_id):
	#TODO:Filter
	#CheckVoters(voters,election_id)
	filtered_voters = []
	try:
		election = Election.objects.get(id=election_id)
		region_names = [region.name for region in election.regions.all()]
		for voter in voters:
			voter_region = PostcodeToRegion(voter[1],election.regions_type)
			if(voter_region in region_names):
				filtered_voters.append(voter)

		return filtered_voters

	except:
		return []
		
def FilterVotersByRegion(voters,region_name,regions_type):
	
	filtered_voters = []
	for voter in voters:
		voter_region = PostcodeToRegion(voter[1],regions_type)
		if(region_name == voter_region):
			filtered_voters.append(voter)
		
	return filtered_voters

def FilterVotersByRegistered(voters,election_id):
	filtered_voters = []
	for voter in voters:
		register_check = VoterAuth.objects.filter(voter_id=voter[0],election_id=election_id)
		if(register_check.count() > 0):
			filtered_voters.append(voter)
	
	return filtered_voters


#STATISTICS

def MakeGraphInstance(graph_title,values_list,graph_num):
	
	return StatGraph(graph_title,values_list,graph_num)


def Demographics(request,election_id):
	authorised,username = CheckAuthorisation(request,True,[('statistics__demographics',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:
		election = 	get_object_or_404(Election, id=election_id)	
		regions = election.regions.all()

		return render(request, 'admin_interface/pages/statistics/view_demographics.html', {'title': "Election Demographics Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks')], "election":election,"regions":regions })


def GetGraph(request,election_id,region_id):
	
	authorised,username = CheckAuthorisation(request,True,[('statistics__demographics',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:
		election = 	get_object_or_404(Election, id=election_id)	
		elegible_voters = AllVoters(election_id)
		registered_voters = FilterVotersByRegistered(elegible_voters,election_id)
		
		

		demographic_statistics = []

		elegible_voters_count = len(elegible_voters)
		registered_voters_count = len(registered_voters)

		demographic_statistics.append( MakeGraphInstance('Election Wide Eligible Voters who Registered Online',[['Did not Register Online',elegible_voters_count-registered_voters_count],['Registered Online',registered_voters_count]],0) )

		region = Region.objects.get(id= region_id)
		i = 1

		region_elegible_voters = FilterVotersByRegion(elegible_voters,region.name,election.regions_type)
		elegible_voters_count = len(region_elegible_voters)

		region_registered_voters = FilterVotersByRegistered(region_elegible_voters,election_id)
		registered_voters_count = len(region_registered_voters)

		demographic_statistics.append( MakeGraphInstance(region.name + ': Eligible Voters who Registered Online',[['Did not Register Online',elegible_voters_count-registered_voters_count],['Registered Online',registered_voters_count]],i+1) )


		return render(request, 'admin_interface/pages/statistics/get_graph.html', {'title': "Election Demographics Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks')], "election":election, "demographic_statistics":demographic_statistics })


def Results(request,election_id,region_id):
	authorised,username = CheckAuthorisation(request,True,[('electoral_officer',)])
	if(not authorised):
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_login')
	else:
		election = get_object_or_404(Election, id=election_id)	
		region = get_object_or_404(Region, id=region_id)	
		
		votes = VoteResults(election_id,region_id)

		processed_results = ProcessResultsFPTP(votes)
		
		graph = MakeGraphInstance(region.name + ': Results for '+region.name,processed_results,1) 


		return render(request, 'admin_interface/pages/results.html', {'title': "Election Results", 'breadcrumb': [("Home", reverse('admin_master_homepage'), 'home'), ("Roles Homepage", reverse('role_homepage'), 'tasks')], "election":election, "processed_results":processed_results,"graph":graph })


def ProcessResultsFPTP(votes):
	candidate_dict = {}

	for vote in votes:
		if(not vote[1] in candidate_dict):
			candidate_dict[vote[1]] = 0
		candidate_dict[vote[1]] += 1

	processed_results = []

	for key,value in candidate_dict.items():
		candidate = Candidate.objects.get(id=key)
		processed_results.append( [candidate.last_name+","+candidate.first_name,value] )

	return processed_results