from django.db import models

class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    #elections = models.ManyToManyField(Candidate, through='ElectionRegion')
    class Meta:
        db_table = 'regions'
        app_label = 'admin'
