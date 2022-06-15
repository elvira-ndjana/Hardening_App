from django.db import models
from procedure.models import Procedure


# Create your models here.
class Controle(models.Model):
    code = models.CharField(max_length=10, null=False)
    libelle = models.CharField(max_length=250, null=False)
    default = models.BooleanField(max_length=10, null=False)
    commande = models.CharField(max_length=10000, null=False)
    verification = models.CharField(max_length=10000, null=False)
    champVerification = models.CharField(max_length=100000, null=False)
    procedure = models.ForeignKey(Procedure, null=True, on_delete=models.SET_NULL)
