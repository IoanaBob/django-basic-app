from .models import Region

def vote_count_fptp(election_id):
    regions = Region.objects.all()
    sum = 0
    for region in regions:
        region_db_name = 'region' + str(region.id)
        try:
            votes_region = RegionVote.using(region_db_name).filter(election_id).count()
            sum += votes_region
        except:
            print("Failed to load votes. Region DB likely Does not exists (This is only for prototype purposes")


def registered_voters(election_id):