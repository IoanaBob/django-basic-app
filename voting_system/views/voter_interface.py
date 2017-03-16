from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404

def homepage(request):
	return render(request, 'voter_interface/homepage.html')

