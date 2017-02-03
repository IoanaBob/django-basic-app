from django.db import models

class Test(models.Model):
    ID = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.ID
    class Meta:
    	app_label = 'auth'