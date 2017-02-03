from django.shortcuts import render
from voting_system.models.test import Test
from .forms import TestForm
from django.shortcuts import redirect, render, get_object_or_404


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