from django.db import models

class VoterAuth(models.Model):
    id = models.IntegerField(primary_key=True)
    voter_code_number = models.IntegerField()
    password_hash = models.CharField(max_length=300)
    class Meta:
        db_table = 'voter_auth'
        app_label = 'auth'