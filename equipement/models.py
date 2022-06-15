from django.db import models


# Create your models here.
class Equipement(models.Model):
    type_equipement = (('routeur', 'routeur'),
                       ('switch', 'switch'),
                       ('serveur', 'serveur')
                       )
    type_systeme = (('windows', 'windows'),
                    ('serveur', 'serveur')
                    )
    nom_equipemen = models.CharField(max_length=50, null=False)
    username_ssh = models.CharField(max_length=50, null=False)
    password_ssh = models.CharField(max_length=50, null=False)
    adresse_ip = models.CharField(max_length=30, null=False)
    type = models.CharField(max_length=30, null=False, choices=type_equipement)
    systeme = models.CharField(max_length=50, null=False, choices=type_systeme)
