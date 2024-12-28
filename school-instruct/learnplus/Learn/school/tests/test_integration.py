import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.apps import apps

# UNIT TESTS


@pytest.mark.django_db
def test_filiere_creation():
    """
    Teste la création d'une instance de Filiere.
    """
    Filiere = apps.get_model('school', 'Filiere')
    filiere = Filiere.objects.create(nom="Informatique")
    assert str(filiere) == "Informatique"
    assert filiere.status is True


@pytest.mark.django_db
def test_instructor_creation():
    """
    Teste la création d'un Instructor avec un utilisateur et une classe associés.
    """
    User = apps.get_model('auth', 'User')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')
    Instructor = apps.get_model('instructor', 'Instructor')

    niveau = Niveau.objects.create(nom="Licence 1")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=1)
    user = User.objects.create_user(username="professeur", password="testpass")

    instructor = Instructor.objects.create(
        user=user,
        contact="0123456789",
        adresse="123 Rue Principale",
        classe=classe,
        photo="path/to/photo.jpg",
        bio="Je suis un enseignant passionné."
    )
    assert str(instructor) == "professeur"
    assert instructor.classe == classe
    assert instructor.contact == "0123456789"


@pytest.mark.django_db
def test_instructor_missing_user():
    """
    Teste la création d'un Instructor sans utilisateur (doit échouer).
    """
    Instructor = apps.get_model('instructor', 'Instructor')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')

    niveau = Niveau.objects.create(nom="Licence 2")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=2)

    with pytest.raises(Exception):
        Instructor.objects.create(
            contact="0123456789",
            adresse="123 Rue Principale",
            classe=classe
        )


@pytest.mark.django_db
def test_instructor_matiere_relation():
    """
    Teste la relation Many-to-Many entre Instructor et Matiere.
    """
    Matiere = apps.get_model('school', 'Matiere')
    Instructor = apps.get_model('instructor', 'Instructor')
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(username="professeur", password="testpass")
    instructor = Instructor.objects.create(
        user=user,
        contact="0123456789",
        adresse="456 Rue Secondaire"
    )
    matiere = Matiere.objects.create(nom="Mathématiques")
    instructor.matieres.add(matiere)
    assert matiere in instructor.matieres.all()


@pytest.mark.django_db
def test_instructor_question_relation():
    """
    Teste la relation Many-to-Many entre Instructor et Question.
    """
    Question = apps.get_model('quiz', 'Question')
    Instructor = apps.get_model('instructor', 'Instructor')
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(username="professeur", password="testpass")
    instructor = Instructor.objects.create(
        user=user,
        contact="0987654321",
        adresse="789 Rue Tertiaire"
    )
    question = Question.objects.create(titre="Qu'est-ce que Python ?")
    instructor.questions.add(question)
    assert question in instructor.questions.all()

# FUNCTIONAL TESTS


@pytest.mark.django_db
def test_login_redirect_authenticated_instructor():
    """
    Teste si un utilisateur authentifié étant instructor est redirigé vers 'dashboard'.
    """
    User = apps.get_model('auth', 'User')
    Instructor = apps.get_model('instructor', 'Instructor')
    user = User.objects.create_user(username="professeur", password="testpass")
    Instructor.objects.create(
        user=user,
        contact="0123456789",
        adresse="456 Rue Secondaire"
    )
    client = Client()
    client.login(username="professeur", password="testpass")
    response = client.get(reverse('login'))
    assert response.status_code == 302  # Redirection
    assert response.url == reverse('dashboard')


@pytest.mark.django_db
def test_protected_view_access_by_instructor():
    """
    Vérifie qu'un instructor authentifié peut accéder à une vue protégée.
    """
    User = apps.get_model('auth', 'User')
    Instructor = apps.get_model('instructor', 'Instructor')
    user = User.objects.create_user(username="professeur", password="testpass")
    Instructor.objects.create(
        user=user,
        contact="0987654321",
        adresse="789 Rue Tertiaire"
    )
    client = Client()
    client.login(username="professeur", password="testpass")
    response = client.get(reverse('protected_view'))
    assert response.status_code == 200

# INTEGRATION TESTS


@pytest.mark.django_db
def test_integration_instructor_classe_and_matiere():
    """
    Teste l'intégration entre Instructor, Classe et Matiere.
    """
    Matiere = apps.get_model('school', 'Matiere')
    Instructor = apps.get_model('instructor', 'Instructor')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')
    User = apps.get_model('auth', 'User')

    niveau = Niveau.objects.create(nom="Licence 3")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=3)
    user = User.objects.create_user(username="professeur", password="testpass")
    instructor = Instructor.objects.create(
        user=user,
        contact="0123456789",
        adresse="123 Rue Principale",
        classe=classe
    )
    matiere = Matiere.objects.create(nom="Histoire")
    instructor.matieres.add(matiere)

    assert instructor.classe == classe
    assert matiere in instructor.matieres.all()
