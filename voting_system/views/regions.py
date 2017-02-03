from django.shortcuts import render
from voting_system.models.region import Region

def regions(request):
    regions = Region.objects.all()
    return render(request, 'admin_interface/regions.html', {'regions': regions})