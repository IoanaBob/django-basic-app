from django.shortcuts import render
from voting_system.models import Region
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