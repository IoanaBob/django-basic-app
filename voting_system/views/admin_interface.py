from django.shortcuts import redirect, render, get_object_or_404
from voting_system.models import Region
from voting_system.models import Candidate
from voting_system.forms import candForm

def regions(request):
    regions = Region.objects.all()
    return render(request, 'admin_interface/regions.html', {'regions': regions})

def candidates(request):
    candidates = Candidate.objects.all()
    return render(request, 'admin_interface/view_candidates.html', {'candidates': candidates})

def newCandidate(request):
    if request.method == "POST":
        form = candForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.id = int(request.user)
            #post.first_name = request.user
            #post.last_name = request.user
            #post.email = request.user
            post.save(using='admin')
            return redirect('candidates')
    else:
        form = candForm()
    return render(request, 'voting_system/new_candidate.html', {'form': form})