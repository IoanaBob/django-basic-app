from django.db import models
from .party import Party
from .region import Region
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45, validators=[RegexValidator(regex="[a-zA-Z]+", message="Candidate name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    last_name = models.CharField(max_length=45, validators=[RegexValidator(regex="[a-zA-Z]+", message="Candidate name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")])
    email = models.EmailField(max_length=60)
    # foreign key
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='party_id')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id')
    
    class Meta:
        db_table = 'candidates'
        app_label = 'admin'