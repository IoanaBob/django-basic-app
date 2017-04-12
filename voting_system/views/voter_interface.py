from django.shortcuts import render
from voting_system.models import VoterCode, VoterAuth
from voting_system.forms import CheckPasswordForm, CheckCodeForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404

def homepage(request):
	return render(request, 'voter_interface/homepage.html')

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
	return render(request, 'voter_interface/homepage.html')

