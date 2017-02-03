from django.shortcuts import render
from voting_system.models.test import Test

def test(request):
	test = Test.objects.using('voterauth').all()
	return render(request, 'voting_system/test.html', {'test': test})