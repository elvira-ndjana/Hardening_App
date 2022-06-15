from django.db import models


# Create your models here.
class Log(models.Model):

    routine = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    type = models.CharField(max_length=100, null=True)
    ip = models.CharField(max_length=500, null=True)
    user = models.CharField(max_length=500, null=True)
    procedure = models.CharField(max_length=10000, null=True)
    rapport = models.CharField(max_length=1000, null=True)
