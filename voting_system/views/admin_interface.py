from django.shortcuts import redirect, render, get_object_or_404
from voting_system.models import Region
from voting_system.models import Candidate
from voting_system.forms.candForm import candForm

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
            candidate = form.save(commit=False)
            #candidate.id = int(request.user)
            candidate.first_name = request.user
            candidate.last_name = request.user
            candidate.email = request.user
            candidate.save()
            return redirect('candidates')
    else:
        form = candForm()
    return render(request, 'admin_interface/new_candidate.html', {'form': form})

def editCandidate(request, id=None):
    candidate = get_object_or_404(Candidate, id=id)
    if request.method == "POST":
        form = candForm(request.POST, instance=candidate)
        if form.is_valid():
            candidate = form.save(commit=False)
            #candidate.id = int(request.user)
            candidate.first_name = request.user
            candidate.last_name = request.user
            candidate.email = request.user
            candidate.save()
            return redirect('candidates')
    else:
        form = candForm(instance=candidate)
    return render(request, 'admin_interface/edit_candidate.html', {'form': form})

def deleteCandidate(request, id=None):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.delete()
    return redirect('candidates')