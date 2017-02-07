from django.shortcuts import render
from voting_system.models import Test
from voting_system.forms import TestForm
from django.shortcuts import redirect, render, get_object_or_404

def test(request):
	test = Test.objects.using('voterauth').all()
	return render(request, 'voting_system/test.html', {'test': test})

def post_new(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.ID = int(request.user)
            #post.name = request.user
            post.save(using='voterauth')
            return redirect('test')
    else:
        form = TestForm()
    return render(request, 'voting_system/post_edit.html', {'form': form})