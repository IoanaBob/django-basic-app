from django.db import models
import requests
import json

class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    #elections = models.ManyToManyField(Candidate, through='ElectionRegion')
    class Meta:
        db_table = 'regions'
        app_label = 'admin'

    def __str__(self):
        return '%s %s' % (self.id, self.name)

    def populate_regions():
        region0 = requests.get(url='http://lda.data.parliament.uk/constituencies.json?exists-endedDate=false&_pageSize=400&_page=0').json()
        region1 = requests.get(url='http://lda.data.parliament.uk/constituencies.json?exists-endedDate=false&_pageSize=400&_page=1').json()
        for i in range(1,651):
            if i<400:
                region_name = region0["result"]["items"][i-1]["label"]["_value"]
            else:
                region_name = region1["result"]["items"][i-401]["label"]["_value"]
            region = Region(id=i, name=region_name)
            region.save()

