from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from voting_system.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from voting_system.forms import LoginForm
from django.contrib.auth.hashers import make_password, check_password
from voting_system.forms import *
from voting_system.forms.admin_formn import *
from voting_system.views.CheckAuthorisation import CheckAuthorisation



from django.db import connection


def CreateDummyUser(request):
    admin_user = Admin()
    admin_user.id = 1
    admin_user.first_name = "John"
    admin_user.last_name = "Smith"
    admin_user.user_name = "j_smith"
    admin_user.password_hash = make_password("abc")
    admin_user.email = "smithj@email.com"
    # foreign key
    
    admin_user.save()

    return render(request, 'admin_interface/login/create_dummy_user.html')
def admin_homepage(request):
	authorised,username = CheckAuthorisation(request,True,[('test_role',)])
	if(authorised):
		return render(request, 'admin_interface/pages/index.html', {'admin': username})
	else:
		return redirect('admin_login')
def admin_view(request):
	admins = Admin.objects.all()
	
	return render(request, 'admin_interface/admin_users/admin_users.html', {'admins': admins,  'first_name':request.session['forename']})

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
			return redirect('admin_users')
	else:
		form = AdminForm(instance=admin)
		
	return render(request, 'admin_interface/admin_users/admin_form.html', {'form': form, 'roles': roles, 'current_roles': role_current,  'first_name':request.session['forename']})
def admin_create(request):
	roles = Role.objects.all()
	if request.method == "POST":
		form = AdminForm(request.POST)
		if form.is_valid():
			if(request.POST.get('password') != request.POST.get('repeatPassword')):
				return render(request, 'admin_interface/admin_users/admin_form.html', {'form': form, 'roles': roles, 'errors': ["Password Does not match"]})
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
		
		return render(request, 'admin_interface/admin_users/admin_form.html', {'form': form, 'roles': roles})

def admin_login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			try:
				user = Admin.objects.get(user_name = request.POST.get('username'))
				if user is not None:
					#removethis check
					if check_password(request.POST.get('password'), user.password_hash):
						request.session['username'] = user.user_name
						request.session['forename'] = user.first_name
						return redirect ('admin_homepage')
					else:
						form = LoginForm()
						return render(request, 'admin_interface/pages/authentication/login.html',{'form': form,'message': "The credentials (pass) does not match our records.", 'title': "Login",'header_messages': {'welcome': "Admin Login"}})
			except Admin.DoesNotExist:
				form = LoginForm()

				return render(request, 'admin_interface/pages/authentication/login.html',{'form': form,'message': "The credentials does not match our records.", 'title': "Login",})
	else:
		form = LoginForm()
		return render(request, 'admin_interface/pages/authentication/login.html',{'form': form,'message': "", 'title': "Login", 'header_messages': {'welcome': "Admin Login"}})

def admin_logout(request):
	try:
		del request.session['username']
	except:
		pass
	
	return render(request, 'admin_interface/login/logged_out.html',{})
	
def populate_regions(request):
	if not Region.objects.all():
		Region.populate_regions()
		return redirect('regions')
	return render(request, 'admin_interface/populate_regions.html', { 'first_name':request.session['forename']})

def regions(request):
	regions = Region.objects.all().order_by('id')
	are_regions = True
	if not regions:
		are_regions = False
	return render(request, 'admin_interface/regions.html', {'regions': regions, 'are_regions': are_regions,  'first_name':request.session['forename']})

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

def voter_codes(request):
	voter_codes = VoterCode.objects.all().order_by('id')
	return render(request, 'admin_interface/voter_codes.html', {'voter_codes': voter_codes})

def candidates(request):
	candidates = Candidate.objects.all().order_by('id')
	return render(request, 'admin_interface/pages/candidates/view.html', {'candidates': candidates, "title": "Candidates", 'first_name':request.session['forename']})

def candidate_create(request):
	if request.method == "POST":
		
		form = CandidateForm(request.POST)
		party = request.POST.get('party_id')
		if form.is_valid():

			candidate = form.save(commit=False)


			candidate.id = getNextID('candidates')
			candidate.party_id = party
			candidate.save()
		return redirect('candidates')
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
			return redirect('candidates')
	else:
		form = CandidateForm(instance=candidate)
		form.fields['party_id'].initial = candidate.party_id

	return render(request, 'admin_interface/pages/candidates/form.html', {'form': form, "title": "Edit Candidate", 'first_name':request.session['forename']})

def candidate_delete(request, id=None):
	candidate = get_object_or_404(Candidate, id=id)
	candidate.delete()
	return redirect('candidates')


def elections(request):

	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		elections = Election.objects.all()
		return render(request, 'admin_interface/pages/elections/elections.html', {'elections': elections,  'first_name':request.session['forename']})
	else:
		message = "You are not authorised to view this page."
		return render(request, 'admin_interface/pages/login/not_authorised.html', {'message': message,  'first_name':request.session['forename']})
def elections_homepage(request):

	authorised,username = CheckAuthorisation(request,True,[("test_role",)])
	if(authorised):
		elections = Election.objects.all()
		return render(request, 'admin_interface/pages/elections/index.html', {'elections': elections,  'first_name':request.session['forename']})
	else:
		message = "You are not authorised to view this page."
		return render(request, 'admin_interface/pages/login/not_authorised.html', {'message': message,  'first_name':request.session['forename']})



def election_create(request):
	if request.method == "POST":
		form = ElectionForm(request.POST)
		if form.is_valid():
			election = form.save(commit=False)
			party.id = getNextID('elections')
			election.save()
			return redirect('elections')
	else:
		form = ElectionForm()
		candidates = Candidate.objects.all()
		regions = Region.objects.all()
	return render(request, 'admin_interface/pages/elections/election_form.html', {'form': form, 'candidates': candidates, 'title': 'Create Election','regions': regions, 'first_name':request.session['forename']})


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
	return render(request, 'admin_interface/elections/election_form.html', {'form': form})


def election_delete(request, id=None):
	election = get_object_or_404(Election, id=id)
	election.delete()
	return redirect('elections')


def roles(request):
	roles = Role.objects.all().order_by('id')
	return render(request, 'admin_interface/roles.html', {'roles' : roles})

def role_create(request):
	if request.method == "POST":
		form = RoleForm(request.POST)
		if form.is_valid():
			role = form.save(commit=False)
			role.id = getNextID('roles')
			
			role.save()
			return redirect('roles')
	else:
		form = RoleForm()
	return render(request, 'admin_interface/role_form.html', {'form': form})

def role_edit(request, id=None):
	role = get_object_or_404(Role, id=id)
	if request.method == "POST":
		form = RoleForm(request.POST, instance=role)
		if form.is_valid():
			role = form.save(commit=False)
			#role.id = request.user
			#role.name = request.user
			role.save()
			return redirect('roles')
	else:
		form = RoleForm(instance=role)
	return render(request, 'admin_interface/role_form.html', {'form': form})

def role_delete(request, id=None):
	role = get_object_or_404(Role, id=id)
	role.delete()
	return redirect('roles')

def party(request):
	parties = Party.objects.all().order_by('id')
	if not parties:
		are_parties = False
	else:
		are_parties = True
	return render(request, 'admin_interface/parties.html', {'parties': parties, 'are_parties': are_parties})

def party_create(request):
	if request.method == "POST":
		form = PartyForm(request.POST)
		if form.is_valid():
			party = form.save(commit=False)
			party.id = getNextID('parties')
			party.save()
			return redirect('party')
	else:
		form = PartyForm()
	return render(request, 'admin_interface/party_form.html', {'form': form})
def party_delete(request, id=None):

	party = get_object_or_404(Party, id=id)
	party.delete()
	return redirect('parties')

def party_edit(request, id=None):
	party = get_object_or_404(Party, id=id)
	if request.method == "POST":
		form = PartyForm(request.POST, instance=party)
		if form.is_valid():
			party = form.save(commit=False)
			
			party.save()
			return redirect('party')
	else:
		form = PartyForm(instance=party)
	return render(request, 'admin_interface/role_form.html', {'form': form})
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
