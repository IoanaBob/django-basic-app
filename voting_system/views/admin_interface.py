from voting_system.models import Region
from voting_system.models import Election
from voting_system.forms import ElectionForm
from django.shortcuts import redirect, render, get_object_or_404

def regions(request):
    regions = Region.objects.all()
    return render(request, 'admin_interface/regions.html', {'regions': regions})


def elections(request):
    elections = Election.objects.all()
    return render(request, 'admin_interface/elections/elections.html', {'elections': elections})


def election_create(request):
    if request.method == "POST":
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            #post.ID = int(request.user)
            #post.name = request.user
            election.save()
            return redirect('elections')
    else:
        form = ElectionForm()
    return render(request, 'admin_interface/elections/election_form.html', {'form': form})


def election_edit(request):
    if request.method == "POST":
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            #post.ID = int(request.user)
            #post.name = request.user
            election.save()
            return redirect('elections')
    else:
        form = ElectionForm()
    return render(request, 'admin_interface/elections/election_form.html', {'form': form})


def election_delete(request):
    if request.method == "POST":
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            #post.ID = int(request.user)
            #post.name = request.user
            election.save()
            return redirect('elections')
    else:
        form = ElectionForm()
    return render(request, 'admin_interface/elections/election_form.html', {'form': form})