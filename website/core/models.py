from django.db import models
from datetime import datetime

# Create your models here.
class Query(models.Model):
    title = models.CharField(max_length=100)
    Last_Crawled = models.DateTimeField(auto_now=True)
    Url = models.URLField(max_length=200, unique=True)
    Description = models.TextField(max_length=500)
    Alexa_Rank = models.IntegerField()
    Keywords = models.CharField(max_length=500)
    robot_txt = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.Alexa_Rank) + ': ' + self.title

class Site_Ranking(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=100, unique=True)
    rank = models.IntegerField()
