from django.db import models
from django.utils import timezone

class Test(models.Model):
    ID = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.ID
    class Meta:
    	app_label = 'authv'

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