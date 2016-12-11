from __future__ import unicode_literals

from django.db import models

# Create your models here.
class type(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return  self.name


class region(models.Model):
   # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class farm (models.Model):
      # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class report(models.Model):
   # id = models.IntegerField(primary_key=True)
    farm = models.ForeignKey(farm, related_name='farm')
    type = models.ForeignKey(type, related_name='type')
    region = models.ForeignKey(region, related_name='region')
    employees = models.IntegerField()
    costs = models.IntegerField()
    profits = models.IntegerField()


