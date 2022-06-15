from django.urls import path
from . import views

urlpatterns = [
    path('connexion/', views.connexion, name='connexion'),
    path('', views.acceuil, name='welcome'),
    path('bord/', views.bord, name='bord'),
    path('informations1/', views.informations, name='bord-informations1'),
    path('informations2/', views.bilan, name='bord-bilan'),
    ]