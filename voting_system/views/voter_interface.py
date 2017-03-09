from django.shortcuts import render

def homepage(request):
	return render(request, 'voter_interface/homepage.html')