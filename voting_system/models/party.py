from django.db import models

class Party(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'parties'
        app_label = 'admin'