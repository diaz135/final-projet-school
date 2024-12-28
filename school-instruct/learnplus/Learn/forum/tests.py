import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse
from django.test import Client
from django.apps import apps

# UNIT TESTS


@pytest.mark.django_db
def test_sujet_creation_without_title():
    """
    Teste que la création d'un sujet sans titre échoue.
    """
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(username="user_fail", password="password")
    Sujet = apps.get_model('forum', 'Sujet')

    with pytest.raises(Exception):
        Sujet.objects.create(
            user=user,
            titre="",  # Pas de titre
            question="Question sans titre"
        )


@pytest.mark.django_db
def test_reponse_creation_with_empty_content():
    """
    Teste que la création d'une réponse avec un contenu vide échoue.
    """
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(username="user_fail_resp", password="password")
    Sujet = apps.get_model('forum', 'Sujet')
    Reponse = apps.get_model('forum', 'Reponse')

    sujet = Sujet.objects.create(
        user=user,
        titre="Sujet sans contenu",
        question="Test pour vérifier"
    )

    with pytest.raises(Exception):
        Reponse.objects.create(
            user=user,
            sujet=sujet,
            contenu=""  # Contenu vide
        )


# FUNCTIONAL TESTS
@pytest.mark.django_db
def test_liste_sujets_view_permissions():
    """
    Vérifie que les utilisateurs non connectés peuvent accéder à la liste des sujets.
    """
    Sujet = apps.get_model('forum', 'Sujet')
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(username="user_view", password="password")

    Sujet.objects.create(
        user=user,
        titre="Sujet visible",
        question="Question publique",
        status=True
    )

    client = Client()
    response = client.get(reverse('liste_sujets'))

    assert response.status_code == 200
    assert "Sujet visible" in response.content.decode()


@pytest.mark.django_db
def test_details_sujet_view_not_found():
    """
    Vérifie qu'une tentative d'accès à un sujet inexistant renvoie une erreur 404.
    """
    client = Client()
    response = client.get(reverse('details_sujet', args=["slug-inexistant"]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_creer_sujet_permission_required():
    """
    Vérifie que seuls les utilisateurs connectés peuvent créer des sujets.
    """
    client = Client()

    data = {
        "titre": "Sujet sans connexion",
        "question": "Question non autorisée"
    }

    response = client.post(reverse('creer_sujet'), data)

    assert response.status_code == 302  # Redirigé vers la page de connexion
    assert "/login" in response.url


@pytest.mark.django_db
def test_ajouter_reponse_permission_required():
    """
    Vérifie que seuls les utilisateurs connectés peuvent ajouter des réponses.
    """
    User = apps.get_model('auth', 'User')
    Sujet = apps.get_model('forum', 'Sujet')
    user = User.objects.create_user(username="user_resp_perm", password="password")

    sujet = Sujet.objects.create(
        user=user,
        titre="Sujet avec permissions",
        question="Test des permissions"
    )

    client = Client()
    data = {"contenu": "Réponse non autorisée"}

    response = client.post(reverse('ajouter_reponse', args=[sujet.slug]), data)

    assert response.status_code == 302  # Redirigé vers la page de connexion
    assert "/login" in response.url


@pytest.mark.django_db
def test_creer_sujet_invalid_data():
    """
    Teste la gestion des erreurs lors de la création d'un sujet avec des données invalides.
    """
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(username="user_invalid", password="password")

    client = Client()
    client.login(username="user_invalid", password="password")

    data = {
        "titre": "",  # Titre vide
        "question": ""  # Question vide
    }

    response = client.post(reverse('creer_sujet'), data)

    Sujet = apps.get_model('forum', 'Sujet')
    sujet = Sujet.objects.filter(titre="").first()

    assert response.status_code == 200  # Resté sur la même page
    assert sujet is None


@pytest.mark.django_db
def test_ajouter_reponse_invalid_data():
    """
    Teste la gestion des erreurs lors de l'ajout d'une réponse avec des données invalides.
    """
    User = apps.get_model('auth', 'User')
    Sujet = apps.get_model('forum', 'Sujet')
    user = User.objects.create_user(username="user_invalid_resp", password="password")

    sujet = Sujet.objects.create(
        user=user,
        titre="Sujet pour réponses invalides",
        question="Tester les erreurs"
    )

    client = Client()
    client.login(username="user_invalid_resp", password="password")

    data = {"contenu": ""}  # Contenu vide
    response = client.post(reverse('ajouter_reponse', args=[sujet.slug]), data)

    Reponse = apps.get_model('forum', 'Reponse')
    reponse = Reponse.objects.filter(contenu="").first()

    assert response.status_code == 302  # Redirection même avec des données invalides
    assert reponse is None


# INTEGRATION TESTS
@pytest.mark.django_db
def test_integration_create_sujet_and_reponse():
    """
    Teste le processus complet de création d'un sujet et d'ajout d'une réponse.
    """
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(username="user_full", password="password")

    client = Client()
    client.login(username="user_full", password="password")

    # Création du sujet
    data_sujet = {
        "titre": "Sujet complet",
        "question": "Question intégrale"
    }
    client.post(reverse('creer_sujet'), data_sujet)

    Sujet = apps.get_model('forum', 'Sujet')
    sujet = Sujet.objects.get(titre="Sujet complet")

    # Ajout d'une réponse
    data_reponse = {
        "contenu": "Réponse complète"
    }
    client.post(reverse('ajouter_reponse', args=[sujet.slug]), data_reponse)

    Reponse = apps.get_model('forum', 'Reponse')
    reponse = Reponse.objects.get(contenu="Réponse complète")

    assert sujet is not None
    assert reponse is not None
    assert reponse.sujet == sujet


@pytest.mark.django_db
def test_example():
    assert 1 + 1 == 2
