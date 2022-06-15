import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from log.models import Log

class HomeView(LoginRequiredMixin, View):

    """HomeView."""
def connexion(request):
    return render(request, 'comptes/connexion.html')

def acceuil(request):
    return render(request, 'comptes/welcome.html')

def bord(request):
    return render(request, 'comptes/home.html')

def informations(request):
    Durcissement = Log.objects.filter(routine="Durcissement").count()
    Conformite = Log.objects.filter(routine="non conformité").count()
    Verifications = Log.objects.filter(routine="Vérification").count()
    Suppression = Log.objects.filter(routine="Suppresion de controle").count()
    Ajout = Log.objects.filter(routine="Ajout de controle").count()
    autres = Ajout + Suppression
    return JsonResponse({"durcissement": Durcissement, "conformite": Conformite, "verifications": Verifications, "autres": autres})

def bilan(request):
    y = str(datetime.date.today().strftime("%Y"))
    m01 = Log.objects.filter(date__contains=y+"-01").count()
    m02 = Log.objects.filter(date__contains=y+"-02").count()
    m03 = Log.objects.filter(date__contains=y+"-03").count()
    m04 = Log.objects.filter(date__contains=y+"-04").count()
    m05 = Log.objects.filter(date__contains=y+"-05").count()
    m06 = Log.objects.filter(date__contains=y+"-06").count()
    m07 = Log.objects.filter(date__contains=y+"-07").count()
    m08 = Log.objects.filter(date__contains=y+"-08").count()
    m09 = Log.objects.filter(date__contains=y+"-09").count()
    m10 = Log.objects.filter(date__contains=y+"-10").count()
    m11 = Log.objects.filter(date__contains=y+"-11").count()
    m12 = Log.objects.filter(date__contains=y+"-12").count()
    return JsonResponse({"m01": m01, "m02": m02, "m03": m03, "m04": m04, "m05": m05, "m06": m06, "m07": m07,
                         "m08": m08, "m09": m09, "m10": m10, "m11": m11, "m12": m12})
