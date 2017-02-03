from django.db import models
from .models import admin, role

class AdminRole(models.Model):
    id = models.IntegerField(primary_key=True)
    admin = models.ForeignKey(Admin, db_column='admin_id')
    role = models.ForeignKey(Role, db_column='role_id')

    class Meta:
        db_table = 'admin_roles'
        app_label = 'admin'