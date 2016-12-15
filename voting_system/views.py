from django.shortcuts import render
from .models import Test

# Create your views here.
def test(request):
	test = Test.objects.using('voterauth').all()
	return render(request, 'voting_system/test.html', {'test': test})
