from django.db import models

class Voter(models.Model):
    id = models.IntegerField(primary_key=True)
    # validators=[RegexValidator(regex="[a-zA-Z]+", message="Role name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")]
    voter_id = models.CharField(max_length=20)   
    title = models.CharField(max_length=10)   
    forname = models.CharField(max_length=40)   
    surname = models.CharField(max_length=40)   
    name_single_line = models.CharField(max_length=90)   
    telephone_number = models.CharField(max_length=15)   
    line_1 = models.CharField(max_length=25)   
    line_2 = models.CharField(max_length=25)   
    line_3 = models.CharField(max_length=25)   
    place = models.CharField(max_length=20)   
    town = models.CharField(max_length=20)   
    postcode = models.CharField(max_length=10)   
    addr_single_line = models.CharField(max_length=125)   

    class Meta:
        db_table = 'voters'
        app_label = 'people'