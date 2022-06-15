from django.urls import path
from . import views

urlpatterns = [
    path('listeEquipemts/', views.list_equipement, name='list-equipement'),
    path('nouvel_equipement/', views.nouvelequipement, name='ajouter-equipement'),
    path('', views.accueil, name='accueil'),
]
