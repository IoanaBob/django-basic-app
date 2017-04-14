from django.db import models
from . import Election, Region, VoterAuth
import random
import string
import requests
import json

class VoterCode(models.Model):
    id = models.IntegerField(primary_key=True, editable=True)
    verified_date = models.DateTimeField(editable=False)
    invalidated_date = models.DateTimeField(editable=False)
    # should set up minumum = maximum length here 
    code = models.CharField(max_length=15, unique = True, editable=True)
    #default false
    sent_status = models.BooleanField(default=False)
    #NEEDS TO CHNAGE TO FOREIGN KEY -- CA ADDED TO TEST VOTER CODES
    voter_id = models.IntegerField(max_length=64)
    # TODO: modify in the DB too!!
    #vote_status = models.BooleanField(default=False)
    # foreign keys
    election = models.ForeignKey(Election, on_delete=models.CASCADE, db_column='election_id')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id')
    class Meta:
        db_table = 'voter_codes'
        app_label = 'admin'

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.id, self.verified_date, self.invalidated_date, self.code, self.vote_status, self.election, self.region)

    def generate_voter_code():
        generated_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        if not VoterCode.objects.filter(code = generated_code).exists():
            return generated_code
        else:
            generate_voter_code();

    def postcode_to_region(postcode):
        postcode = postcode.replace(" ", "")
        # fake postcode - from the people API
        if postcode == "YO913X0":
            return Region.objects.get(name = "Cardiff Central")
        else:
            data = requests.get(url = 'https://api.postcodes.io/postcodes/' + postcode).json()
            region_name = data["result"]["parliamentary_constituency"] 
            return Region.objects.get(name = region_name)


    def populate_voter_codes(the_election):
        data = requests.get(url = "http://t2a.co/rest/?output=json&method=person_search&api_key=test").json()
        data = data["person_list"]
        if VoterCode.objects.exists():
            i = VoterCode.objects.latest('id').id + 1
        else:
            i = 1
        for person in data:
            voter_code = VoterCode.generate_voter_code()
            region = VoterCode.postcode_to_region(person["postcode"])
            VoterAuth.save_password(i)
            entry = VoterCode(id=i, code=voter_code, election = the_election, region = region)
            entry.save()
            i += 1