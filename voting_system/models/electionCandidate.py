from django.db import models
from .models import election, candidate

class ElectionCandidate(models.Model):
    id = models.IntegerField(primary_key=True)
    election = models.ForeignKey(Election, db_column='election_id')
    candidate = models.ForeignKey(Candidate, db_column='candidate_id')
    class Meta:
        db_table = 'election_candidates'
        app_label = 'admin'
