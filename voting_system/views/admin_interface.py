from django.shortcuts import render
from voting_system.models import Region

def regions(request):
    regions = Region.objects.all()
    return render(request, 'admin_interface/regions.html', {'regions': regions})