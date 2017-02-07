from django.db import models
from .election import Election
from .region import Region
import random

class VoterCode(models.Model):
    id = models.IntegerField(primary_key=True)
    verified_date = models.DateTimeField()
    invalidated_date = models.DateTimeField()
    # should set up minumum = maximum length here 
    code = models.CharField(max_length=15, unique = True)
    #default false
    # TODO: modify in the DB too!!
    vote_status = models.BooleanField()
    # foreign keys
    election = models.ForeignKey(Election, on_delete=models.CASCADE, db_column='election_id')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id')
    class Meta:
        db_table = 'voter_codes'
        app_label = 'admin'

    def generate_voter_code():
        generated_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        if not VoterCode.objects.filter(code = generated_code).exists():
            return generated_code
        else:
            generate_voter_code();