from voting_system.models import Region
from voting_system.models import Election
from voting_system.forms import ElectionForm
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import redirect, render, get_object_or_404

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
