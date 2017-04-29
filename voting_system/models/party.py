from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Party(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, validators=[RegexValidator(regex="[a-zA-Z]+", message="Party name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    class Meta:
        db_table = 'parties'
        app_label = 'admin'