from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from voting_system.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from voting_system.forms import *
from voting_system.views.CheckAuthorisation import CheckAuthorisation
from django.contrib import messages

from django.core.paginator import Paginator
from django.db import connection
from django.conf import settings


def admin_master_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		return render(request, 'admin_interface/pages/index.html', {'admin': username})
	else:
		return redirect('admin_login')
#---- Authentication START ----#
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
						return render(request, 'admin_interface/pages/authentication/login.html',{'form': form, 'title': "Login",'header_messages': {'welcome': "Admin Login"}})
			except Admin.DoesNotExist:
				form = LoginForm()
				messages.error(request, "Your credentials does not match our records.")
				return render(request, 'admin_interface/pages/authentication/login.html',{'form': form, 'title': "Login",})
	else:
		form = LoginForm()
		return render(request, 'admin_interface/pages/authentication/login.html',{'form': form,'message': "", 'title': "Login", 'header_messages': {'welcome': "Admin Login"}})

def admin_logout(request):
	try:
		del request.session['username']
		del request.session['forename']
	except:
		pass
	
	messages.success(request, "You have been successfully logged out")
	return render(request, 'voter_interface/pages/homepage.html',{})

#---- Authentication END ----#


#---- Admin START ----#
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
		return render(request, 'admin_interface/pages/admin/view.html', {'title': "View Admins", 'admins': admins,  'first_name':request.session['forename']})
	else:
		message.error(request, "Access Denied. You do not have sufficient privileges.")
		return render(request, 'admin_interface/pages/index.html', {  'first_name':request.session['forename']})
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
		return render(request, 'admin_interface/pages/admin/view.html', {'title': "View Admins", 'admins': admins,  'first_name':request.session['forename']})
	else:
		message.error(request, "Access Denied. You do not have sufficient privileges.")
		return render(request, 'admin_interface/pages/index.html', {  'first_name':request.session['forename']})
def admins_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		return render(request, 'admin_interface/pages/admin/index.html', {'first_name': request.session['forename']})
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
		
		return render(request, 'admin_interface/pages/admin/form.html', {'form': form, 'roles': roles})

def admin_delete(request, id=None):
	admin = get_object_or_404(Admin, id=id)
	admin.delete()
	messages.error(request, "Admin #"+id+" has been deleted!")
	return redirect('admin_view')
#---- Admin END ----#

#---- Voter Code START ----#
def voter_code_homepage(requests):
	return render(request, 'admin_interface/pages/codes/index.html')
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
		return render(request, 'admin_interface/pages/codes/view.html', {'title': "View Voter Codes", 'voter_codes': voter_codes,  'first_name':request.session['forename']})
	else:
		message.error(request, "Access Denied. You do not have sufficient privileges.")
		return render(request, 'admin_interface/pages/index.html', {  'first_name':request.session['forename']})
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
		return render(request, 'admin_interface/pages/codes/view.html', {'title': "View Voter Codes", 'voter_codes': voter_codes,  'first_name':request.session['forename']})
	else:
		message.error(request, "Access Denied. You do not have sufficient privileges.")
		return render(request, 'admin_interface/pages/index.html', {  'first_name':request.session['forename']})
#---- Voter Code END ----#
	
#---- MISC START (TO SORTT) ----#

# DEPRECATED
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


#---- Candidates START ----#

def candidate_homepage(request):
	return render(request, 'admin_interface/pages/candidates/index.html', {"title": "Candidates Homepage", 'first_name':request.session['forename']})
def candidate_view(request):
	candidate_list = Candidate.objects.all().order_by('id')
	paginator = Paginator(candidate_list, settings.PAGINATION_LENGTH)

	try:
		candidates = paginator.page(1)
	except PageNotAnInteger:
		candidates = paginator.page(1)
	except EmptyPage:
		candidates = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/candidates/view.html', {'title': "View Candidates", 'candidates':candidates,  'first_name':request.session['forename']})
def candidate_view_page(request, page_id=None):
	candidate_list = Candidate.objects.all().order_by('id')
	paginator = Paginator(candidate_list, settings.PAGINATION_LENGTH)
	try:
		candidates = paginator.page(page_id)
	except PageNotAnInteger:
		candidates = paginator.page(1)
	except EmptyPage:
		candidates = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/candidates/view.html', {'title': "View Candidates", 'candidates': candidates,  'first_name':request.session['forename']})

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
		return render(request, 'admin_interface/pages/candidates/form.html', {'form': form,  "title": "New Candidate", 'first_name':request.session['forename']})

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

	return render(request, 'admin_interface/pages/candidates/form.html', {'form': form, "title": "Edit Candidate", 'first_name':request.session['forename']})

def candidate_delete(request, id=None):
	candidate = get_object_or_404(Candidate, id=id)
	candidate.delete()
	messages.error(request, "Candidate #"+id+" has been deleted!")
	return redirect('candidate_view')


#---- Candidates END ----#

#---- Election START ----#
def election_homepage(request):

	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		elections = Election.objects.all()
		return render(request, 'admin_interface/pages/elections/index.html', {'elections': elections,  'first_name':request.session['forename']})
	else:
		message = "You are not authorised to view this page."
		return render(request, 'admin_interface/pages/login/not_authorised.html', {'message': message,  'first_name':request.session['forename']})




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
		return render(request, 'admin_interface/pages/elections/view.html', {'title': "View Elections", 'elections': elections,  'first_name':request.session['forename']})
	else:
		message.error(request, "Access Denied. You do not have sufficient privileges.")
		return render(request, 'admin_interface/pages/index.html', {  'first_name':request.session['forename']})
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
		return render(request, 'admin_interface/pages/elections/view.html', {'title': "View Elections", 'elections': elections,  'first_name':request.session['forename']})
	else:
		message.error(request, "Access Denied. You do not have sufficient privileges.")
		return render(request, 'admin_interface/pages/index.html', {  'first_name':request.session['forename']})
def election_create(request):
	candidates = Candidate.objects.all()
	if request.method == "POST":
		form = ElectionForm(request.POST)
		if form.is_valid():
			election = form.save(commit=False)
			election.id = getNextID('elections')
			election.save()
			messages.success(request, "Successfully added new Election!")
			return redirect('election_view')
	else:
		form = ElectionForm()
		regions = Region.objects.all()
	
	return render(request, 'admin_interface/pages/elections/form.html', {'form': form, 'candidates': candidates, 'title': 'Create Election','regions': regions, 'first_name':request.session['forename']})


def election_edit(request, id=None):
	election = get_object_or_404(Election, id=id)
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
	return render(request, 'admin_interface/pages/elections/form.html', {'form': form, 'candidates': candidates, 'title': 'Edit Election','regions': regions, 'first_name':request.session['forename']})


def election_delete(request, id=None):
	election = get_object_or_404(Election, id=id)
	election.delete()
	messages.error(request, "Election #"+id+" has been Deleted")
	return redirect('election_view')
#---- Election END ----#

#---- Role START ----#
def role_homepage(request):
	return render(request, 'admin_interface/pages/roles/index.html')
def role_view(request):
	roles_list = Role.objects.all().order_by('id')
	paginator = Paginator(roles_list, settings.PAGINATION_LENGTH)

	try:
		roles = paginator.page(1)
	except PageNotAnInteger:
		roles = paginator.page(1)
	except EmptyPage:
		roles = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/roles/view.html', {'title': "View Roles", 'roles': roles,  'first_name':request.session['forename']})
def role_view_page(request, page_id=None):
	roles_list = Role.objects.all().order_by('id')
	paginator = Paginator(roles_list, settings.PAGINATION_LENGTH)
	try:
		roles = paginator.page(page_id)
	except PageNotAnInteger:
		roles = paginator.page(1)
	except EmptyPage:
		roles = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/roles/view.html', {'title': "View Roles", 'roles': roles,  'first_name':request.session['forename']})
def role_create(request):
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
	return render(request, 'admin_interface/pages/roles/form.html', {'form': form})

def role_edit(request, id=None):
	role = get_object_or_404(Role, id=id)
	if request.method == "POST":
		form = RoleForm(request.POST, instance=role)
		if form.is_valid():
			role = form.save(commit=False)
			#role.id = request.user
			#role.name = request.user
			role.save()
			messages.success(request, "Role #"+id+" Successfully Updated!")
			return redirect('role_view')
	else:
		form = RoleForm(instance=role)
	return render(request, 'admin_interface/pages/roles/form.html', {'form': form})

def role_delete(request, id=None):
	role = get_object_or_404(Role, id=id)
	role.delete()
	MESSAGE_TAGS = {
		messages.error: 'danger'
	}
	messages.error(request, "Role #"+id+" has been deleted!")
	return redirect('role_view')
#---- Role END ----#

#---- Party START---#
def party_homepage(request):
	return render(request, 'admin_interface/pages/parties/index.html', {'title': "Party Homepage"})

def party_view(request):
	party_list = Party.objects.all().order_by('id')
	paginator = Paginator(party_list, settings.PAGINATION_LENGTH)

	try:
		parties = paginator.page(1)
	except PageNotAnInteger:
		parties = paginator.page(1)
	except EmptyPage:
		parties = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/parties/view.html', {'parties': parties,  'first_name':request.session['forename']})	
def party_view_page(request, page_id=None):
	party_list = Party.objects.all().order_by('id')
	paginator = Paginator(party_list, settings.PAGINATION_LENGTH)
	try:
		parties = paginator.page(page_id)
	except PageNotAnInteger:
		parties = paginator.page(1)
	except EmptyPage:
		parties = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/parties/view.html', {'parties': parties,  'first_name':request.session['forename']})	

def party_create(request):
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
	return render(request, 'admin_interface/pages/parties/form.html', {'form': form})
def party_delete(request, id=None):

	party = get_object_or_404(Party, id=id)
	party.delete()
	messages.error(request, "Party #"+id+" has been deleted!")
	return redirect('party_view')

def party_edit(request, id=None):
	party = get_object_or_404(Party, id=id)
	if request.method == "POST":
		form = PartyForm(request.POST, instance=party)
		if form.is_valid():
			party = form.save(commit=False)
			
			party.save()
			return redirect('party_view')
	else:
		form = PartyForm(instance=party)
	return render(request, 'admin_interface/pages/parties/form.html', {'form': form})
def party_view_page(request, page_id=None):
	party_list = Party.objects.all().order_by('id')
	paginator = Paginator(party_list, 25)
	try:
		parties = paginator.page(page_id)
	except PageNotAnInteger:
		parties = paginator.page(1)
	except EmptyPage:
		parties = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/parties/view.html', {'parties': parties,  'first_name':request.session['forename']})	
#---- Party  END---#

# -----  Region -----#
def region_homepage(request):
	return render(request, 'admin_interface/pages/regions/index.html', {"title": "Regions Homepage", 'first_name': request.session['forename']})
def region_view(request):
	
	regions_list = Region.objects.all().order_by('id')
	paginator = Paginator(regions_list, settings.PAGINATION_LENGTH)

	try:
		regions = paginator.page(1)
	except PageNotAnInteger:
		regions = paginator.page(1)
	except EmptyPage:
		regions = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/regions/view.html', {'title': "View Regions", 'regions': regions,  'first_name':request.session['forename']})

def region_view_page(request, page_id=None):
	regions_list = Region.objects.all().order_by('id')
	paginator = Paginator(regions_list, settings.PAGINATION_LENGTH)

	try:
		regions = paginator.page(page_id)
	except PageNotAnInteger:
		regions = paginator.page(1)
	except EmptyPage:
		regions = paginator.page(paginator.num_pages)
	return render(request, 'admin_interface/pages/regions/view.html', {'title': "View Regions", 'regions': regions,  'first_name':request.session['forename']})
def region_create(request):
	if request.method == "POST":
		form = RegionForm(request.POST)
		if form.is_valid():
			region = form.save(commit=False)
			region.id = getNextID('region')
			region.save()
			return redirect('region_view')
	else:
		form = RegionForm()
	return render(request, 'admin_interface/pages/regions/form.html', {'form': form})
def region_edit(request, id=None):
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
	return render(request, 'admin_interface/pages/regions/form.html', {'form': form})
def region_populate(request):
	if not Region.objects.all():
		Region.populate_regions()
		messages.success(request, "Regions successfuly populate!")
		return redirect('regions_view')
	else :
		messages.error(request, "Regions could not be populated")
		return redirect( 'regions_view', { 'first_name': request.session['forename']})

def region_delete(request, id=None):

	region = get_object_or_404(Region, id=id)
	region.delete()
	messages.error(request, "Region #"+id+" successfuly deleted!")
	return redirect('region_view')
#---- Region END ---#

def getNextID(tblName):
	cursor = connection.cursor()
	cursor.execute( "select nextval('"+tblName+"_id_seq')")
	row = cursor.fetchone()
	cursor.close()
	return row[0]

def isEmpty(elements):
	count = 0

	for element in elements:
		count += 1
	return {0: True}.get(count, False)
