from django.db import models


# Create your models here.
class Procedure(models.Model):
    nom = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=300, null=False)
    type_equipement = models.CharField(max_length=20, null=False)
    systeme = models.CharField(max_length=300, null=False)

