from django.urls import path
from . import views

urlpatterns = [
    path('listeProcedures/', views.liste_procedures, name='liste-procedure'),
    path('correctionNonConformite/', views.correction_conformite, name='non-conformite'),
    path('rechercheProcedure/', views.recherche_procedure, name='recherche-procedure'),
    path('executerProcedure/', views.executer_procedure, name='executer-procedure'),
    path('executerConformite/', views.executer_conformite, name='executer-procedure'),
    path('avancementProcedure/', views.avancement, name='avancement-procedure'),
]