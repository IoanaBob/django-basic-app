from django.db import models

### In reality, 650

# Class member names MUST correspond with the info inside the
# region votes table in the main database.
# Otherwise, they can't be Queried!!!

class Region1Votes(models.Model):
    id = models.IntegerField(primary_key=True)
    election_id = models.IntegerField()
    candidate_id = models.IntegerField()
    candidate_count = models.IntegerField()

    class Meta:
        db_table = 'region1_votes'
        app_label = 'reg1'