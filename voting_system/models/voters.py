from django.db import models
import random
import string
import requests
import json

class Voter(models.Model):
    id = models.IntegerField(primary_key=True)
    # validators=[RegexValidator(regex="[a-zA-Z]+", message="Role name must only contain the following characters: a-z	A-Z	àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð, . ‘ -", code="invalid name")]
    voter_id = models.CharField(max_length=20)   
    title = models.CharField(max_length=10)   
    forename = models.CharField(max_length=40)   
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

    def generate_voter_id():
        generated_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        if not Voter.objects.filter(voter_id = generated_id).exists():
            return generated_id
        else:
            generate_voter_id()

    def populate_voters():
        data = requests.get(url = "http://t2a.co/rest/?output=json&method=person_search&api_key=test").json()
        data = data["person_list"]
        i = 1
        for person in data:
            if not "surname" in person:
                the_surname = ""
            else:
                the_surname = person["surname"]
            voterid = Voter.generate_voter_id()
            entry = Voter(id=i, voter_id=voterid, title = person["title"], forename = person["forename"], surname = the_surname, name_single_line = person["name_single_line"], telephone_number = person["telephone_number"], line_1 = person["line_1"], line_2 = person["line_2"], line_3 = person["line_3"], place = person["place"], town = person["town"], postcode = person["postcode"], addr_single_line = person["addr_single_line"])
            entry.save(using='people')
            i += 1