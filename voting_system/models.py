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
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    userName = models.CharField(max_length=30)
    password_hash = models.CharField(max_length=300)
    email = models.CharField(max_length=60)
    # foreign key
    roles = models.ManyToManyField(Role)
    class Meta:
        db_table = 'admins'
        app_label = 'admin'

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'roles'
        app_label = 'admin'

class Party(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'parties'
        app_label = 'admin'

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    # foreign key
    candidate = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='candidate_id')
    class Meta:
        db_table = 'candidates'
        app_label = 'admin'

class Election(models.Model):
    id = models.IntegerField(primary_key=True)
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField()
    #uninominal or secret voting =>
    # if uninominal true, if secret false
    uninominalVoting = models.BooleanField()
    #foreign keys
    parties = models.ManyToManyField(Party)
    candidates = models.ManyToManyField(Candidate)
    class Meta:
        db_table = 'elections'
        app_label = 'admin'

class VoterCode(models.Model):
    id = models.IntegerField(primary_key=True)
    verifiedDate = models.DateTimeField()
    invalidatedDate = models.DateTimeField()
    registeredNumber = models.IntegerField()
    # should set up minumum = maximum length here 
    code = models.CharField(max_length=15)
    # foreign keys
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
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
    regionNumber = models.IntegerField()
    password_hash = models.CharField(max_length=300)
    class Meta:
        db_table = 'voter_auth'
        app_label = 'auth'


########################################################
### Sample tables for the regions inside the country ###
########################################################

### In reality, 660

# Region id names of the table MUST correspond with the info inside the
# region table in the main database.
# Otherwise, they can't be Queried!!!
class Region1Name(models.Model):
    id = models.IntegerField(primary_key=True)
    electionId = models.IntegerField()
    candidateId = models.IntegerField()
    candidateCount = models.IntegerField()

    class Meta:
        db_table = 'region1_name'
        app_label = 'reg1'

class Region2Name(models.Model):
    id = models.IntegerField(primary_key=True)
    electionId = models.IntegerField()
    candidateId = models.IntegerField()
    candidateCount = models.IntegerField()

    class Meta:
        db_table = 'region2_name'
        app_label = 'reg2'


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