from django.shortcuts import render, redirect, render, get_object_or_404

def homepage(request):

	return render(request, 'voter_interface/homepage.html')

def check_code(request):
	return render(request, '')




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
