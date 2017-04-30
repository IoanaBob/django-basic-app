from django.db import models
from django.utils import timezone
from .party import Party
from .candidate import Candidate
from .region import Region

class Election(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    #uninominal or secret voting =>
    # if uninominal voting = true, if party list = false
    uninominal_voting = models.BooleanField()
    # if secret voting, is true
    #secret_voting = models.BooleanField()
    election_method = models.CharField(max_length=20, choices=( ('fptp', 'First Past the Post'), ('stv','Single Transferable Vote')))
    #foreign keys
    parties = models.ManyToManyField(Party, through='ElectionParty')
    candidates = models.ManyToManyField(Candidate, through='ElectionCandidate')
    regions = models.ManyToManyField(Region, through='ElectionRegion')

    def __str__(self):
        return '%s; from: %s; to: %s' % (self.name, self.start_date, self.end_date)

    class Meta:
        db_table = 'elections'
        app_label = 'admin'