from django.shortcuts import get_object_or_404, redirect
from forum.models import Sujet, Reponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Sujet, Reponse

# Liste des sujets disponibles dans le forum


def liste_sujets(request):
    sujets = Sujet.objects.filter(status=True).order_by('-date_add')  # Filtre les sujets actifs
    return render(request, 'pages/instructor-forum.html', {'sujets': sujets})

# Détails d'un sujet spécifique


def details_sujet(request, slug):
    sujet = get_object_or_404(Sujet, slug=slug, status=True)  # Vérifie que le sujet existe et est actif
    reponses = Reponse.objects.filter(sujet=sujet, status=True).order_by('date_add')  # Filtre les réponses actives
    return render(request, 'pages/instructor-forum-thread.html', {'forum': sujet, 'reponses': reponses})

# Permet de créer un nouveau sujet


@login_required
def creer_sujet(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        question = request.POST.get('question')
        if titre and question:  # Vérifie que les champs requis sont remplis
            Sujet.objects.create(
                user=request.user,
                titre=titre,
                question=question
            )
            return redirect('liste_sujets')  # Redirige vers la liste des sujets
    return render(request, 'pages/instructor-forum-ask.html')

# Permet d'ajouter une réponse à un sujet existant


@login_required
def ajouter_reponse(request, slug):
    sujet = get_object_or_404(Sujet, slug=slug, status=True)
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:  # Vérifie que le champ n'est pas vide
            Reponse.objects.create(
                user=request.user,
                sujet=sujet,
                contenu=contenu
            )
            return redirect('details_sujet', slug=sujet.slug)
    return redirect('details_sujet', slug=sujet.slug)


@login_required
def ajouter_reponse(request, slug):
    sujet = get_object_or_404(Sujet, slug=slug, status=True)  # Récupère le sujet correspondant au slug
    if request.method == 'POST':
        contenu = request.POST.get('contenu')  # Récupère le champ "contenu" du formulaire
        if contenu:  # Vérifie que le contenu n'est pas vide
            Reponse.objects.create(
                user=request.user,
                sujet=sujet,
                contenu=contenu
            )
            return redirect('details_sujet', slug=sujet.slug)  # Redirige vers les détails du sujet
    return redirect('details_sujet', slug=sujet.slug)
