from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from equipement.models import Equipement
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):

    """HomeView."""

def list_equipement(request):
    equipements = Equipement.objects.all()  # recuperation de toutes les lignes dans la table procedures
    if request.method == 'POST':
        if 'rechercher' in request.POST:
            equipements  = Equipement.objects.filter(id=request.POST.get('id'),type=request.POST.get('type')).values()
        elif 'voir_tout' in request.POST:
            equipements = Equipement.objects.all()
    context = {'equipements': equipements}
    return render(request, 'equipements/list_equipement.html', context)

def nouvelequipement(request):
    context ={}
    if request.method == 'POST':
        equipement = Equipement()
        equipement.nom_equipemen = request.POST.get('nom')
        equipement.username_ssh= request.POST.get('username')
        equipement.password_ssh= request.POST.get('password')
        equipement.adresse_ip = request.POST.get('adresseip')
        equipement.type = request.POST.get('type')
        equipement.systeme = request.POST.get('systeme')
        equipement.save()
        log = Log()
        log.nom = "Enregistrement de l'equipement "+request.POST.get('nom')
        log.type_operation = "Enregistremnet d'appareils"
        log.nom_utilisateur = username
        log.save()
        messages.success(request, 'Votre equipement a bien ete ajoute!')


    return render(request, 'equipements/ajouter_un_equipement.html')

def accueil(request):
    return render(request, 'index.html')