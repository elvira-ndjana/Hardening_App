from django.urls import path
from . import views

urlpatterns = [
    path('liste_contrôles/', views.liste_controles, name='liste_contrôles'),
    path('ajouter_contrôle/', views.ajouter_controle, name='ajouter_controle'),
    path('recherche_contrôle/', views.recherche_controle, name='recherher_controle'),
    path('suppression_contrôle/', views.supprimer_controle, name='supprimer_controle'),
    path('verification_contrôle/', views.verification_controle, name='verifications_controle'),
    path('executer_verification/', views.executer_verification, name='executer_verifications'),
    path('rechercheProcedure/', views.recherche_procedure, name='recherche-procedure'),
    path('avancementVerification/', views.avancement, name='avancement-procedure'),
]