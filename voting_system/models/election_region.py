from django.db import models
from .election import Election
from .region import Region

class ElectionRegion(models.Model):
    id = models.IntegerField(primary_key=True)
    election = models.ForeignKey(Election, db_column='election_id')
    region = models.ForeignKey(Region, db_column='region_id')
    class Meta:
        db_table = 'election_regions'
        app_label = 'admin'