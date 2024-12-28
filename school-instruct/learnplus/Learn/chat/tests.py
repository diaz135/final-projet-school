import pytest
from django.urls import reverse
from django.apps import apps
from django.test import Client

# UNIT TESTS


@pytest.mark.django_db
def test_create_salon():
    """
    Teste la création d'un salon.
    """
    User = apps.get_model('auth', 'User')
    Salon = apps.get_model('chat', 'Salon')

    user = User.objects.create_user(username="chat_user", password="password")
    salon = Salon.objects.create(
        nom="Salon Test",
        classe=None,
    )

    assert Salon.objects.count() == 1
    assert salon.nom == "Salon Test"
    assert salon.slug is not None


@pytest.mark.django_db
def test_create_message():
    """
    Teste la création d'un message dans un salon.
    """
    User = apps.get_model('auth', 'User')
    Salon = apps.get_model('chat', 'Salon')
    Message = apps.get_model('chat', 'Message')

    user = User.objects.create_user(username="chat_user", password="password")
    salon = Salon.objects.create(nom="Salon Test", classe=None)
    message = Message.objects.create(
        user=user,
        salon=salon,
        contenu="Bonjour tout le monde !"
    )

    assert Message.objects.count() == 1
    assert message.contenu == "Bonjour tout le monde !"
    assert message.salon == salon
    assert message.user == user


@pytest.mark.django_db
def test_salon_creation_without_name():
    """
    Teste que la création d'un salon sans nom échoue.
    """
    Salon = apps.get_model('chat', 'Salon')

    with pytest.raises(Exception):
        Salon.objects.create(nom="")

# FUNCTIONAL TESTS


@pytest.mark.django_db
def test_access_salon_view():
    """
    Teste que les utilisateurs connectés peuvent accéder à un salon.
    """
    User = apps.get_model('auth', 'User')
    Salon = apps.get_model('chat', 'Salon')

    user = User.objects.create_user(username="user_chat", password="password")
    salon = Salon.objects.create(nom="Salon Test", classe=None)

    client = Client()
    client.login(username="user_chat", password="password")
    response = client.get(reverse('chat_salon', args=[salon.slug]))

    assert response.status_code == 200
    assert "pages/chat-salon.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_send_message_view():
    """
    Teste l'envoi de messages dans un salon.
    """
    User = apps.get_model('auth', 'User')
    Salon = apps.get_model('chat', 'Salon')
    Message = apps.get_model('chat', 'Message')

    user = User.objects.create_user(username="user_chat", password="password")
    salon = Salon.objects.create(nom="Salon Test", classe=None)

    client = Client()
    client.login(username="user_chat", password="password")

    data = {"contenu": "Message de test"}
    response = client.post(reverse('chat_send_message', args=[salon.slug]), data)

    assert response.status_code == 302
    assert Message.objects.count() == 1
    assert Message.objects.first().contenu == "Message de test"


@pytest.mark.django_db
def test_access_salon_without_login():
    """
    Teste qu'un utilisateur non connecté ne peut pas accéder à un salon.
    """
    Salon = apps.get_model('chat', 'Salon')

    salon = Salon.objects.create(nom="Salon Test", classe=None)

    client = Client()
    response = client.get(reverse('chat_salon', args=[salon.slug]))

    assert response.status_code == 302
    assert "/login" in response.url


@pytest.mark.django_db
def test_view_messages_in_salon():
    """
    Teste que les messages d'un salon sont correctement affichés.
    """
    User = apps.get_model('auth', 'User')
    Salon = apps.get_model('chat', 'Salon')
    Message = apps.get_model('chat', 'Message')

    user = User.objects.create_user(username="user_chat", password="password")
    salon = Salon.objects.create(nom="Salon Test", classe=None)
    Message.objects.create(user=user, salon=salon, contenu="Premier message")
    Message.objects.create(user=user, salon=salon, contenu="Deuxième message")

    client = Client()
    client.login(username="user_chat", password="password")
    response = client.get(reverse('chat_salon', args=[salon.slug]))

    assert response.status_code == 200
    assert "Premier message" in str(response.content)
    assert "Deuxième message" in str(response.content)

# INTEGRATION TESTS


@pytest.mark.django_db
def test_complete_chat_flow():
    """
    Teste le flux complet : création de salon, envoi et récupération des messages.
    """
    User = apps.get_model('auth', 'User')
    Salon = apps.get_model('chat', 'Salon')
    Message = apps.get_model('chat', 'Message')

    user = User.objects.create_user(username="user_flow", password="password")
    salon = Salon.objects.create(nom="Salon Intégration", classe=None)

    client = Client()
    client.login(username="user_flow", password="password")

    # Envoi de message
    data = {"contenu": "Message d'intégration"}
    client.post(reverse('chat_send_message', args=[salon.slug]), data)

    # Récupération des messages
    response = client.get(reverse('chat_salon', args=[salon.slug]))
    assert response.status_code == 200
    assert "Message d'intégration" in str(response.content)


@pytest.mark.django_db
def test_invalid_message_submission():
    """
    Teste que l'envoi d'un message vide échoue.
    """
    User = apps.get_model('auth', 'User')
    Salon = apps.get_model('chat', 'Salon')

    user = User.objects.create_user(username="user_invalid", password="password")
    salon = Salon.objects.create(nom="Salon Invalid", classe=None)

    client = Client()
    client.login(username="user_invalid", password="password")

    data = {"contenu": ""}  # Contenu vide
    response = client.post(reverse('chat_send_message', args=[salon.slug]), data)

    assert response.status_code == 200
    assert "Ce champ est requis" in str(response.content)
