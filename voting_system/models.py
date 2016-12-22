from django.db import models
from django.utils import timezone

class Test(models.Model):
    ID = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.ID
    class Meta:
    	app_label = 'auth'


#############################
### admin database tables ###
#############################

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

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'roles'
        app_label = 'admin'

class AdminRole(models.Model):
    id = models.IntegerField(primary_key=True)
    admin = models.ForeignKey(Admin, db_column='admin_id')
    role = models.ForeignKey(Role, db_column='role_id')

    class Meta:
        db_table = 'admin_roles'
        app_label = 'admin'

class Party(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'parties'
        app_label = 'admin'

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    # foreign key
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='party_id')
    class Meta:
        db_table = 'candidates'
        app_label = 'admin'

class Election(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    #uninominal or secret voting =>
    # if uninominal voting = true, if party list = false
    uninominal_voting = models.BooleanField()
    # if secret voting, is true
    secret_voting = models.BooleanField()
    #foreign keys
    parties = models.ManyToManyField(Party, through='ElectionParty')
    candidates = models.ManyToManyField(Candidate, through='ElectionCandidate')
    class Meta:
        db_table = 'elections'
        app_label = 'admin'

class ElectionParty(models.Model):
    id = models.IntegerField(primary_key=True)
    election = models.ForeignKey(Election, db_column='election_id')
    party = models.ForeignKey(Party, db_column='party_id')
    class Meta:
        db_table = 'election_parties'
        app_label = 'admin'

class ElectionCandidate(models.Model):
    id = models.IntegerField(primary_key=True)
    election = models.ForeignKey(Election, db_column='election_id')
    candidate = models.ForeignKey(Party, db_column='candidate_id')
    class Meta:
        db_table = 'election_candidates'
        app_label = 'admin'

class VoterCode(models.Model):
    id = models.IntegerField(primary_key=True)
    verified_date = models.DateTimeField()
    invalidated_date = models.DateTimeField()
    registered_number = models.CharField()
    # should set up minumum = maximum length here 
    code = models.CharField(max_length=15)
    # foreign keys
    election = models.ForeignKey(Election, on_delete=models.CASCADE, db_column='election_id')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id')
    class Meta:
        db_table = 'voter_codes'
        app_label = 'admin'

class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'regions'
        app_label = 'admin'


#################################
### voterauth database tables ###
#################################

class VoterAuth(models.Model):
    id = models.IntegerField(primary_key=True)
    registration_number = models.IntegerField()
    password_hash = models.CharField(max_length=300)
    class Meta:
        db_table = 'voter_auth'
        app_label = 'auth'


########################################################
### Sample tables for the regions inside the country ###
########################################################

### In reality, 660

# Class member names MUST correspond with the info inside the
# region votes table in the main database.
# Otherwise, they can't be Queried!!!
class Region1Votes(models.Model):
    id = models.IntegerField(primary_key=True)
    election_id = models.IntegerField()
    candidate_id = models.IntegerField()
    candidate_count = models.IntegerField()

    class Meta:
        db_table = 'region1_votes'
        app_label = 'reg1'

class Region2Votes(models.Model):
    id = models.IntegerField(primary_key=True)
    election_id = models.IntegerField()
    candidate_id = models.IntegerField()
    candidate_count = models.IntegerField()

    class Meta:
        db_table = 'region2_votes'
        app_label = 'reg2'


# sample model, will be deleted later
'''
class Admin(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
# Create your models here.
'''