from django.urls import path
from . import views

urlpatterns = [
    path('listelog/', views.liste_log, name='liste-log'),
    path('recherche_logs/', views.recherche_logs, name='recherche-log'),
    ]