from __future__ import unicode_literals

from django.db import models

# Create your models here.
class users(models.Model):
    #id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    type = models.IntegerField

    def __str__(self):
        return  self.login + " " +self.password




