from django.db import models
from .role import Role

class Admin(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=30)
    password_hash = models.CharField(max_length=300)
    email = models.CharField(max_length=60)
    # foreign key
    roles = models.ManyToManyField(Role, through='AdminRole')
    class Meta:
        db_table = 'admins'
        app_label = 'admin'