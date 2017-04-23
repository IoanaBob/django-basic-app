from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Verify(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, validators=[RegexValidator(regex="[a-zA-Z]+", message="Verify name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    last_name = models.CharField(max_length=50, validators=[RegexValidator(regex="[a-zA-Z]+", message="Verify name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    voter_id = models.CharField(max_length=50, validators=[RegexValidator(regex="[a-zA-Z]+", message="Verify voter id must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid username")])
    password_hash = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    
    class Meta:
        db_table = 'users'
        app_label = 'gov_verify'

class VerifyLogin(models.Model):
	email = models.CharField(max_length=50)
	password = models.CharField(max_length=200)