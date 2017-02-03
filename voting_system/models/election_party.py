from django.db import models
from .models import election, party

class ElectionParty(models.Model):
    id = models.IntegerField(primary_key=True)
    election = models.ForeignKey(Election, db_column='election_id')
    party = models.ForeignKey(Party, db_column='party_id')
    class Meta:
        db_table = 'election_parties'
        app_label = 'admin'
