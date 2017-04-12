from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, validators=[RegexValidator(regex="[a-zA-Z]+", message="Role name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    class Meta:
        db_table = 'roles'
        app_label = 'admin'
