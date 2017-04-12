from django.db import models
from .role import Role
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Admin(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45, validators=[RegexValidator(regex="[a-zA-Z]+", message="Admin name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    last_name = models.CharField(max_length=45, validators=[RegexValidator(regex="[a-zA-Z]+", message="Admin name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    user_name = models.CharField(max_length=30, validators=[RegexValidator(regex="[a-zA-Z]+", message="Admin username must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid username")])
    password_hash = models.CharField(max_length=300)
    email = models.EmailField(max_length=60)
    # foreign key
    roles = models.ManyToManyField(Role, through='AdminRole')
    class Meta:
        db_table = 'admins'
        app_label = 'admin'