from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from voting_system.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from voting_system.forms import *
from voting_system.views.CheckAuthorisation import CheckAuthorisation
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.conf import settings


def admin_master_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		return render(request, 'admin_interface/pages/index.html', {'title': "Login", 'breadcrumb': [("Home", reverse('admin_master_homepage'))], 'first_name': request.session['forename']})
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
					if request.POST.get('password') == user.password_hash:
						request.session['username'] = user.user_name
						request.session['forename'] = user.first_name.capitalize()
						messages.success(request, "Welcome! You have been successfully logged in!")
						return redirect ('admin_homepage')
					else:
						form = LoginForm()
						messages.error(request, "Your credentials does not match our records.")
						return render(request, 'admin_interface/pages/authentication/login.html',{'title': "Login",'breadcrumb': [("Home", reverse('admin_master_homepage')), ('Login', reverse('admin_login'))], 'form': form, 'welcome': "Admin Login"})
			except Admin.DoesNotExist:
				form = LoginForm()
				messages.error(request, "Your credentials does not match our records.")
				return render(request, 'admin_interface/pages/authentication/login.html',{ 'title': "Login",'breadcrumb': [("Home", reverse('admin_master_homepage')), ('Login', reverse('admin_login'))], 'form': form})
	else:
		form = LoginForm()
		return render(request, 'admin_interface/pages/authentication/login.html',{'title': "Login", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ('Login', reverse('admin_login'))], 'welcome': "Admin Login", 'form': form})

def admin_logout(request):
	try:
		del request.session['username']
		del request.session['forename']
	except:
		pass
	
	messages.success(request, "You have been successfully logged out")
	return redirect ('public_vote__home')

# ---- Authentication END ---- #

# ---- Admin START ---- #
def admin_view(request):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		admin_list = Admin.objects.all().order_by('id')
		paginator = Paginator(admin_list, settings.PAGINATION_LENGTH)
		try:
			admins = paginator.page(1)
		except PageNotAnInteger:
			admins = paginator.page(1)
		except EmptyPage:
			admins = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/admin/view.html', {'title': "View Admins", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Admin Homepage", reverse('admin_homepage')), ('View',  reverse('admin_view'))],  'first_name':request.session['forename'], 'admins': admins})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_homepage')
def admin_view_page(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		admin_list = Admin.objects.all().order_by('id')
		paginator = Paginator(admin_list, settings.PAGINATION_LENGTH)
		try:
			admins = paginator.page(page_id)
		except PageNotAnInteger:
			admins = paginator.page(1)
		except EmptyPage:
			admins = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/admin/view.html', {'title': "View Admins", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Admin Homepage", reverse('admin_homepage')), ('View',  reverse('admin_view'))],  'first_name':request.session['forename'], 'admins': admins})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_homepage')
def admins_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		return render(request, 'admin_interface/pages/admin/index.html', {'title': 'Admin Homepage','breadcrumb': [("Home", reverse('admin_master_homepage')), ("Admin Homepage", reverse('admin_homepage'))], 'first_name': request.session['forename']})
	else:
		return redirect('admin_login')
def admin_edit(request, id =None):
	admin = get_object_or_404(Admin, id=id)
	role_current = AdminRole.objects.filter(admin_id = id).values_list("role_id", flat=True)
	roles = Role.objects.all()

	if request.method == "POST":

		form = AdminForm(request.POST, instance=admin)
		if form.is_valid():
			admin = form.save(commit=False)
			selected_roles = request.POST.getlist('roles[]')


			# Dirty way... 
			# Remove all previous roles for admin then assign new ones -- TALK TO ME ABOUT THIS -- need a more efficienet way 
			AdminRole.objects.filter(admin_id = id).delete()
			
			for role in selected_roles:
				new_role = AdminRole()
				new_role.id = getNextID("admin_roles")
				new_role.admin_id = id
				new_role.role_id = role
				new_role.save()
			admin.save()
			return redirect('admin_view')
	else:
		form = AdminForm(instance=admin)
		
	return render(request, 'admin_interface/pages/admin/form.html', {'form': form, 'roles': roles, 'current_roles': role_current,  'first_name':request.session['forename']})
def admin_create(request):
	roles = Role.objects.all()
	if request.method == "POST":
		form = AdminForm(request.POST)
		if form.is_valid():
			if(request.POST.get('password') != request.POST.get('repeatPassword')):
				return render(request, 'admin_interface/pages/admin/form.html', {'form': form, 'roles': roles, 'errors': ["Password Does not match"]})
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
			
				return redirect('admin_users')
	else:
		form = AdminForm()
		
		return render(request, 'admin_interface/pages/admin/form.html', {'title': 'Create new Admin', 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Admin Homepage", reverse('admin_homepage')), ("Create new Admin", reverse('admin_create'))], 'first_name': request.session['forename'], 'form': form, 'roles': roles})

def admin_delete(request, id=None):
	admin = get_object_or_404(Admin, id=id)
	admin.delete()
	messages.error(request, "Admin #"+id+" has been deleted!")
	return redirect('admin_view')
# ---- Admin END ---- #

# ---- Voter Code START ---- #
def voter_code_homepage(request):
	return render(request, 'admin_interface/pages/codes/index.html', {'title': "Voter Code Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Voter Codes Homepage", reverse('voter_code_homepage'))], 'first_name': request.session['forename']})
def voter_code_view(request):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		codes_list = VoterCode.objects.all().order_by('id')
		paginator = Paginator(codes_list, settings.PAGINATION_LENGTH)
		try:
			voter_codes = paginator.page(1)
		except PageNotAnInteger:
			voter_codes = paginator.page(1)
		except EmptyPage:
			voter_codes = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/codes/view.html', {'title': "View Voter Codes", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Voter Codes Homepage", reverse('voter_code_homepage')), ("View Voter Codes", reverse('voter_code_view'))], 'first_name':request.session['forename'], 'voter_codes': voter_codes  })
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('voter_code_homepage')

def voter_code_view_page(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		codes_list = VoterCode.objects.all().order_by('id')
		paginator = Paginator(codes_list, settings.PAGINATION_LENGTH)
		try:
			voter_codes = paginator.page(page_id)
		except PageNotAnInteger:
			voter_codes = paginator.page(1)
		except EmptyPage:
			voter_codes = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/codes/view.html', {'title': "View Voter Codes", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Voter Codes Homepage", reverse('voter_code_homepage')), ("View Voter Codes", reverse('voter_code_view'))], 'first_name':request.session['forename'], 'voter_codes': voter_codes})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('voter_code_homepage')

# ---- Voter Code END ---- #
	
# ---- MISC START (TO SORTT) ---- #

# ---- Candidates START ---- #
def candidate_homepage(request):
	return render(request, 'admin_interface/pages/candidates/index.html', {"title": "Candidates Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Candidate Homepage", reverse('candidate_homepage'))], 'first_name':request.session['forename']})
def candidate_view(request):
	candidate_list = Candidate.objects.all().order_by('id')
	paginator = Paginator(candidate_list, settings.PAGINATION_LENGTH)

	try:
		candidates = paginator.page(1)
	except PageNotAnInteger:
		candidates = paginator.page(1)
	except EmptyPage:
		candidates = paginator.page(paginator.num_pages)

	return render(request, 'admin_interface/pages/candidates/view.html', {'title': "View Candidates", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Candidate Homepage", reverse('candidate_homepage')), ("View Candidates", reverse('candidate_view'))], 'candidates':candidates,  'first_name':request.session['forename']})
def candidate_view_page(request, page_id=None):
	candidate_list = Candidate.objects.all().order_by('id')
	paginator = Paginator(candidate_list, settings.PAGINATION_LENGTH)
	try:
		candidates = paginator.page(page_id)
	except PageNotAnInteger:
		candidates = paginator.page(1)
	except EmptyPage:
		candidates = paginator.page(paginator.num_pages)
	
	return render(request, 'admin_interface/pages/candidates/view.html', {'title': "View Candidates", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Candidate Homepage", reverse('candidate_homepage')), ("View Candidates", reverse('candidate_view'))], 'candidates':candidates,  'first_name':request.session['forename']})

def candidate_create(request):
	if request.method == "POST":
		
		form = CandidateForm(request.POST)
		party = request.POST.get('party_id')
		if form.is_valid():

			candidate = form.save(commit=False)
			candidate.id = getNextID('candidates')
			candidate.party_id = party
			candidate.save()
			messages.success(request, "Successfully added a new candidiate!")
		return redirect('candidate_view')
	else:
		form = CandidateForm()
		return render(request, 'admin_interface/pages/candidates/form.html', {"title": "Create Candidate", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Candidate Homepage", reverse('candidate_homepage')), ("Create new Candidate", reverse('candidate_create'))],  'first_name':request.session['forename'], 'form': form })

def candidate_edit(request, id=None):
	candidate = get_object_or_404(Candidate, id=id)
	if request.method == "POST":
		form = CandidateForm(request.POST, instance=candidate)
		if form.is_valid():
			candidate = form.save(commit=False)
			candidate.save()
			messages.success(request, "Candidate #"+id+" successfully update!")
			return redirect('candidate_view')
	else:
		form = CandidateForm(instance=candidate)
		form.fields['party_id'].initial = candidate.party_id

	return render(request, 'admin_interface/pages/candidates/form.html', { "title": "Edit Candidate", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Candidate Homepage", reverse('candidate_homepage')), ("Edit Candidate", reverse('candidate_edit',kwargs={'id':id}))], 'first_name':request.session['forename'], 'form': form})

def candidate_delete(request, id=None):
	candidate = get_object_or_404(Candidate, id=id)
	candidate.delete()
	messages.error(request, "Candidate #"+id+" has been deleted!")
	return redirect('candidate_view')


# ---- Candidates END ---- #

# ---- Election START ---- #
def election_homepage(request):

	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		elections = Election.objects.all()
		return render(request, 'admin_interface/pages/elections/index.html', {"title": 'Election Homepage', 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Election Homepage", reverse('election_homepage'))],'first_name':request.session['forename'], 'elections': elections })
	else:
		message = "You are not authorised to view this page."
		return redirect('election_homepage')




def election_view(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		election_list = Election.objects.all().order_by('id')
		paginator = Paginator(election_list, settings.PAGINATION_LENGTH)

		try:
			elections = paginator.page(1)
		except PageNotAnInteger:
			elections = paginator.page(1)
		except EmptyPage:
			elections = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/elections/view.html', {'title': "View Elections", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Election Homepage", reverse('election_homepage')), ("View Elections", reverse('election_view'))],'first_name':request.session['forename'], 'elections': elections})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')
def election_view_page(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		election_list = Election.objects.all().order_by('id')
		paginator = Paginator(election_list, settings.PAGINATION_LENGTH)
		try:
			elections = paginator.page(page_id)
		except PageNotAnInteger:
			elections = paginator.page(1)
		except EmptyPage:
			elections = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/elections/view.html', {'title': "View Elections", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Election Homepage", reverse('election_homepage')), ("View Elections", reverse('election_view'))],'first_name':request.session['forename'], 'elections': elections})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')
def election_create(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
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
				selected_regions = request.POST.getlist('regions[]')
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
	
		return render(request, 'admin_interface/pages/elections/form.html', {'title': 'Create Election', 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Election Homepage", reverse('election_homepage')), ("Create new Election", reverse('election_create'))],'first_name': request.session['forename'], 'form': form, 'regions': regions,'candidates': candidates})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')

def election_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		election = get_object_or_404(Election, id=id)
		candidates_current = ElectionCandidate.objects.filter(election_id = id).values_list("candidate_id", flat=True)
		region_current = ElectionRegion.objects.filter(election_id = id).values_list("region_id", flat=True)
		if request.method == "POST":
			form = ElectionForm(request.POST, instance=election)
			if form.is_valid():
				election = form.save(commit=False)
				election.save()
				return redirect('elections')
		else:
			form = ElectionForm(instance=election)
			candidates = Candidate.objects.all()
			regions = Region.objects.all()
		return render(request, 'admin_interface/pages/elections/form.html', {'title': 'Create Election', 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Election Homepage", reverse('election_homepage')), ("Edit Election", reverse('election_edit',kwargs={'id':id}))],'first_name': request.session['forename'], 'form': form, 'regions': regions,'candidates': candidates, 'current_candidates': candidates_current,'current_regions':region_current })
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')

def election_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		election = get_object_or_404(Election, id=id)
		election.delete()
		messages.error(request, "Election #"+id+" has been Deleted")
		return redirect('election_view')
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('election_homepage')
# ---- Election END ---- #

# ---- Role START ---- #
def role_homepage(request):
	return render(request, 'admin_interface/pages/roles/index.html', {'title': "Roles Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Roles Homepage", reverse('role_homepage'))], 'first_name':request.session['forename'] })
def role_view(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		roles_list = Role.objects.all().order_by('id')
		paginator = Paginator(roles_list, settings.PAGINATION_LENGTH)

		try:
			roles = paginator.page(1)
		except PageNotAnInteger:
			roles = paginator.page(1)
		except EmptyPage:
			roles = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/roles/view.html', {'title': "View Roles", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Roles Homepage", reverse('role_homepage')), ("View Role", reverse('role_view'))], 'first_name':request.session['forename'], 'roles': roles})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_homepage')
def role_view_page(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		roles_list = Role.objects.all().order_by('id')
		paginator = Paginator(roles_list, settings.PAGINATION_LENGTH)
		try:
			roles = paginator.page(page_id)
		except PageNotAnInteger:
			roles = paginator.page(1)
		except EmptyPage:
			roles = paginator.page(paginator.num_pages)
		
		return render(request, 'admin_interface/pages/roles/view.html', {'title': "View Roles", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Roles Homepage", reverse('role_homepage')), ("View Role", reverse('role_view'))], 'first_name':request.session['forename'], 'roles': roles})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_homepage')
def role_create(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
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
		return render(request, 'admin_interface/pages/roles/form.html', {'title': "Create new Role",  'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Roles Homepage", reverse('role_homepage')), ("Create new Role", reverse('role_create'))], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_homepage')
def role_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
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
			return render(request, 'admin_interface/pages/roles/form.html', {'title': "Edit new Role",  'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Roles Homepage", reverse('role_homepage')), ("Edit Role")], 'first_name':request.session['forename'], 'form': form})
		return render(request, 'admin_interface/pages/roles/form.html', {'title': "Edit new Role",  'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Roles Homepage", reverse('role_homepage')), ("Edit Role")], 'first_name':request.session['forename'], 'form': form})
	else :
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_view')

def role_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		role = get_object_or_404(Role, id=id)
		role.delete()
		messages.error(request, "Role #"+id+" has been deleted!")
		return redirect('role_view')
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('role_view')
# ---- Role END ---- #

# ---- Party START--- #
def party_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		return render(request, 'admin_interface/pages/parties/index.html', {'title': "Party Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Parties Homepage", reverse('party_homepage'))], 'first_name':request.session['forename']})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_master_homepage')
def party_view(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		party_list = Party.objects.all().order_by('id')
		paginator = Paginator(party_list, settings.PAGINATION_LENGTH)

		try:
			parties = paginator.page(1)
		except PageNotAnInteger:
			parties = paginator.page(1)
		except EmptyPage:
			parties = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/parties/view.html', {'title': "Party Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Parties Homepage", reverse('party_homepage'))], 'first_name':request.session['forename'], 'parties': parties,})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_homepage')
def party_view_page(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		party_list = Party.objects.all().order_by('id')
		paginator = Paginator(party_list, settings.PAGINATION_LENGTH)
		try:
			parties = paginator.page(page_id)
		except PageNotAnInteger:
			parties = paginator.page(1)
		except EmptyPage:
			parties = paginator.page(paginator.num_pages)
		return render(request, 'admin_interface/pages/parties/view.html', {'title': "Party Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Parties Homepage", reverse('party_homepage'))], 'first_name':request.session['forename'], 'parties': parties,})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_homepage')
def party_create(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
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
		return render(request, 'admin_interface/pages/parties/form.html', {'title': "Create new Party", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Parties Homepage", reverse('party_homepage')), ("Create new Party", reverse('party_create'))], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_homepage')
def party_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		party = get_object_or_404(Party, id=id)
		party.delete()
		messages.error(request, "Party #"+id+" has been deleted!")
		return redirect('party_view')
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_homepage')

def party_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
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
		return render(request, 'admin_interface/pages/parties/form.html', {'title': "Create new Party", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Parties Homepage", reverse('party_homepage')), ("Create new Party", reverse('party_create'))], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('party_view')

# ---- Party  END--- #

# -----  Region ----- #
def region_view(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		return render(request, 'admin_interface/pages/regions/index.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Region Homepage", reverse('region_homepage'))], 'first_name':request.session['forename']})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('admin_master_homepage')
	
def region_view(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		regions_list = Region.objects.all().order_by('id')
		paginator = Paginator(regions_list, settings.PAGINATION_LENGTH)
		try:
			regions = paginator.page(1)
		except PageNotAnInteger:
			regions = paginator.page(1)
		except EmptyPage:
			regions = paginator.page(paginator.num_pages)

		return render(request, 'admin_interface/pages/regions/view.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Region Homepage", reverse('region_homepage')), ("View Regions", reverse('region_view'))], 'first_name':request.session['forename'], 'regions': regions})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')

def region_view_page(request, page_id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		regions_list = Region.objects.all().order_by('id')
		paginator = Paginator(regions_list, settings.PAGINATION_LENGTH)

		try:
			regions = paginator.page(page_id)
		except PageNotAnInteger:
			regions = paginator.page(1)
		except EmptyPage:
			regions = paginator.page(paginator.num_pages)

		return render(request, 'admin_interface/pages/regions/view.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Region Homepage", reverse('region_homepage')), ("View Regions", reverse('region_view'))], 'first_name':request.session['forename'], 'regions': regions})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')
def region_create(request):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
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
		return render(request, 'admin_interface/pages/regions/form.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Region Homepage", reverse('region_homepage')), ("Create new region", reverse('region_create'))], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')
def region_edit(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
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
		return render(request, 'admin_interface/pages/regions/form.html', {'title': "Regions Homepage", 'breadcrumb': [("Home", reverse('admin_master_homepage')), ("Region Homepage", reverse('region_homepage')), ("Edit Region", reverse('region_edit'))], 'first_name':request.session['forename'], 'form': form})
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')

def region_delete(request, id=None):
	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		region = get_object_or_404(Region, id=id)
		region.delete()
		messages.error(request, "Region #"+id+" successfuly deleted!")
		return redirect('region_view')
	else:
		messages.error(request, "Access Denied. You do not have sufficient privileges.")
		return redirect('region_homepage')
# ---- Region END --- #

def getNextID(tblName):
	cursor = connection.cursor()
	cursor.execute( "select nextval('"+tblName+"_id_seq')")
	row = cursor.fetchone()
	cursor.close()
	return row[0]

# ---- Misc Functions START --- #
'''def generate_buttons_page_menu(page_name):

	allowed_pages = {'admin_master_homepage' : [('asd', 'asd')],
					'admin_homepage': [('asd','asd')],
					'election_homepage',
					'voter_code_homepage',
					'party_homepage',
					'region_homepage',
					'candidate_homepage'}
	# Check if menu is in allowed_list

	buttons = []
	if page_name in allowed_pages:
		#probably better from stratch 
		# get list of roles
		#GetUserRoles(rquest.session['username'])

		#for role in roles:

			#if page_name contains role:
			
				#add into buttons using ('button name', button reverse(url_name)


	#else:
		#return False
'''
# ---- Misc Functions END --- #

# don't move these functions or change their names. I am working on them.
# -- okay -- I've changed the region popuate to generated correct ID with sequences - CA

def populate_voter_codes(request):
	if request.method == "POST":
		form = VoterCodeForm(request.POST)
		if form.is_valid():
			election = form.instance.election
			form.save(commit=False)
			print(election)
			VoterCode.populate_voter_codes(election)
			return redirect('elections')
	else:
		form = VoterCodeForm()
	return render(request, 'admin_interface/populate_voter_codes.html', {'form': form})

def region_populate(request):
	if not Region.objects.all():
		Region.populate_regions()
		messages.success(request, "Regions successfuly populated!")
		return redirect('region_view')
	else :
		messages.error(request, "Regions are already populated.")
		return redirect( 'region_view', { 'first_name': request.session['forename']})