from django.shortcuts import render, redirect, render, get_object_or_404

def homepage(request):

	return render(request, 'voter_interface/homepage.html')

def check_code(request):
	return render(request, '')
