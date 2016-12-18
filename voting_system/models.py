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
    password_hash = models.CharField()
    email = models.CharField(max_length=60)

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

class Party(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.CharField(max_length=60)

class Election(models.Model):
    id = models.IntegerField(primary_key=True)
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField()
    #uninominal or secret voting =>
    # if uninominal true, if secret false
    uninominalVoting = models.BooleanField()

class VoterCode(models.Model):
    id = models.IntegerField(primary_key=True)
    verifiedDate = models.DateTimeField()
    invalidatedDate = models.DateTimeField()
    registeredNumber = models.IntegerField()
    # should set up minumum = maximum length here => I put 15
    code = models.CharField(min_length=15, max_length=15)

class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)


#################################
### voterauth database tables ###
#################################

class VoterAuth(models.Model):
    id = models.IntegerField(primary_key=True)
    regionNumber = models.IntegerField()
    password_hash = models.CharField()


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
        app_label = 'reg1'

class Region2Name(models.Model):
    id = models.IntegerField(primary_key=True)
    electionId = models.IntegerField()
    candidateId = models.IntegerField()
    candidateCount = models.IntegerField()

    class Meta:
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