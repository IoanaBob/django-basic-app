from django.db import models


class RegionVote(models.Model):
    id = models.IntegerField(primary_key=True)
    election_id = models.IntegerField()
    candidate_id = models.IntegerField()
    ballot_id = models.IntegerField()
    rank = models.IntegerField()
