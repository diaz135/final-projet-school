from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_sujets, name='liste_sujets'),  # Affiche la liste des sujets
    path('sujet/<slug:slug>/', views.details_sujet, name='details_sujet'),  # Affiche les détails d'un sujet
    path('sujet/nouveau/', views.creer_sujet, name='creer_sujet'),  # Permet de créer un nouveau sujet
    path('sujet/<slug:slug>/repondre/', views.ajouter_reponse, name='ajouter_reponse'),  # Ajoute une réponse à un sujet
]
