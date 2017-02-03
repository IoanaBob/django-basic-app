from django.db import models

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'roles'
        app_label = 'admin'
