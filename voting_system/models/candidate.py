from django.db import models
from .party import Party

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    # foreign key
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='party_id')
    class Meta:
        db_table = 'candidates'
        app_label = 'admin'