from django.shortcuts import redirect, render, get_object_or_404
from voting_system.models import Region
from voting_system.models import Candidate
from voting_system.forms.candForm import candForm
from voting_system.models import Election
from voting_system.forms import ElectionForm


def populate_regions(request):
    if not Region.objects.all():
        Region.populate_regions()
        return redirect('regions')
    return render(request, 'admin_interface/populate_regions.html')

def regions(request):
    regions = Region.objects.all()
    are_regions = True
    if not regions:
        are_regions = False
    return render(request, 'admin_interface/regions.html', {'regions': regions, 'are_regions': are_regions})

def candidates(request):
    candidates = Candidate.objects.all()
    return render(request, 'admin_interface/view_candidates.html', {'candidates': candidates})

def candidate_create(request):
    if request.method == "POST":
        form = candForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.save()
            return redirect('candidates')
    else:
        form = candForm()
    return render(request, 'admin_interface/candidate_form.html', {'form': form})

def candidate_edit(request, id=None):
    candidate = get_object_or_404(Candidate, id=id)
    if request.method == "POST":
        form = candForm(request.POST, instance=candidate)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.save()
            return redirect('candidates')
    else:
        form = candForm(instance=candidate)
    return render(request, 'admin_interface/candidate_form.html', {'form': form})

def candidate_delete(request, id=None):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.delete()
    return redirect('candidates')


def elections(request):
    elections = Election.objects.all()
    return render(request, 'admin_interface/elections/elections.html', {'elections': elections})


def election_create(request):
    if request.method == "POST":
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            election.save()
            return redirect('elections')
    else:
        form = ElectionForm()
    return render(request, 'admin_interface/elections/election_form.html', {'form': form})


def election_edit(request, id=None):
    election = get_object_or_404(Election, id=id)
    if request.method == "POST":
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            election = form.save(commit=False)
            election.save()
            return redirect('elections')
    else:
        form = ElectionForm(instance=election)
    return render(request, 'admin_interface/elections/election_form.html', {'form': form})


def election_delete(request, id=None):
    election = get_object_or_404(Election, id=id)
    election.delete()
    return redirect('elections')


