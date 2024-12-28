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
def test_filiere_creation_invalid():
    """
    Teste la création d'une Filiere avec un nom vide.
    """
    Filiere = apps.get_model('school', 'Filiere')
    with pytest.raises(Exception):
        Filiere.objects.create(nom="")


@pytest.mark.django_db
def test_matiere_slug_creation():
    """
    Teste la génération automatique du slug pour Matiere.
    """
    Matiere = apps.get_model('school', 'Matiere')
    matiere = Matiere.objects.create(nom="Python Avancé")
    assert matiere.slug.startswith("python-avance")


@pytest.mark.django_db
def test_niveau_str_method():
    """
    Teste la méthode __str__ pour Niveau.
    """
    Niveau = apps.get_model('school', 'Niveau')
    niveau = Niveau.objects.create(nom="Licence 1")
    assert str(niveau) == "Licence 1"


@pytest.mark.django_db
def test_classe_creation():
    """
    Teste la création d'une Classe avec Niveau et Filiere.
    """
    Niveau = apps.get_model('school', 'Niveau')
    Filiere = apps.get_model('school', 'Filiere')
    Classe = apps.get_model('school', 'Classe')
    niveau = Niveau.objects.create(nom="Master 1")
    filiere = Filiere.objects.create(nom="Informatique")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=1, filiere=filiere)
    assert str(classe) == "Master 1 1"
    assert classe.filiere == filiere


@pytest.mark.django_db
def test_chapitre_creation():
    """
    Teste la création d'un Chapitre avec un slug valide.
    """
    Chapitre = apps.get_model('school', 'Chapitre')
    chapitre = Chapitre.objects.create(titre="Introduction aux Matrices")
    assert str(chapitre) == "Introduction aux Matrices"
    assert chapitre.slug.startswith("introduction-aux-matrices")


@pytest.mark.django_db
def test_cours_creation():
    """
    Teste la création d'un Cours avec un Chapitre associé.
    """
    Chapitre = apps.get_model('school', 'Chapitre')
    Cours = apps.get_model('school', 'Cours')
    chapitre = Chapitre.objects.create(titre="Chapitre 1")
    cours = Cours.objects.create(titre="Cours 1 - Les bases", chapitre=chapitre)
    assert str(cours) == "Cours 1 - Les bases"
    assert cours.chapitre == chapitre


@pytest.mark.django_db
def test_matiere_instructor_relation():
    """
    Teste la relation Many-to-Many entre Matiere et Instructor.
    """
    Matiere = apps.get_model('school', 'Matiere')
    Instructor = apps.get_model('instructor', 'Instructor')
    matiere = Matiere.objects.create(nom="Mathématiques")
    instructor = Instructor.objects.create(name="Prof. Einstein")
    matiere.instructor.add(instructor)
    assert instructor in matiere.instructor.all()

# FUNCTIONAL TESTS


@pytest.mark.django_db
def test_login_redirect_authenticated_student():
    """
    Teste si un utilisateur authentifié étant étudiant est redirigé vers 'index_student'.
    """
    user = User.objects.create_user(username="studentuser", password="testpass")
    client = Client()
    client.login(username="studentuser", password="testpass")
    response = client.get(reverse('login'))
    assert response.status_code == 302  # Redirection


@pytest.mark.django_db
def test_login_render_guest_login_page():
    """
    Teste si un utilisateur non authentifié voit la page de connexion invité.
    """
    client = Client()
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'pages/guest-login.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_signup_redirect_authenticated_student():
    """
    Teste si un utilisateur authentifié étant étudiant est redirigé vers 'index_student'.
    """
    user = User.objects.create_user(username="studentuser", password="testpass")
    client = Client()
    client.login(username="studentuser", password="testpass")
    response = client.get(reverse('guests_signup'))
    assert response.status_code == 302  # Redirection


@pytest.mark.django_db
def test_forgot_password_redirect_authenticated_student():
    """
    Teste si un utilisateur authentifié étant étudiant est redirigé vers 'index_student'.
    """
    user = User.objects.create_user(username="studentuser", password="testpass")
    client = Client()
    client.login(username="studentuser", password="testpass")
    response = client.get(reverse('forgot_password'))
    assert response.status_code == 302  # Redirection


@pytest.mark.django_db
def test_islogin_success():
    """
    Teste si un utilisateur peut se connecter avec un nom d'utilisateur et un mot de passe corrects.
    """
    user = User.objects.create_user(username="testuser", password="testpass")
    client = Client()
    data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post(reverse('post'), data, content_type="application/json")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True


@pytest.mark.django_db
def test_islogin_failure():
    """
    Teste si une tentative de connexion avec des identifiants incorrects échoue.
    """
    client = Client()
    data = {
        "username": "wronguser",
        "password": "wrongpass"
    }
    response = client.post(reverse('post'), data, content_type="application/json")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is False
    assert response_data["message"] == "Vos identifiants ne sont pas correcte"


@pytest.mark.django_db
def test_deconnexion():
    """
    Teste si un utilisateur peut se déconnecter correctement.
    """
    user = User.objects.create_user(username="testuser", password="testpass")
    client = Client()
    client.login(username="testuser", password="testpass")
    response = client.get(reverse('deconnexion'))
    assert response.status_code == 302  # Redirection
    assert response.url == reverse('login')

# INTEGRATION TESTS


@pytest.mark.django_db
def test_integration_create_filiere_and_classe():
    """
    Teste l'intégration entre Filiere et Classe.
    """
    Filiere = apps.get_model('school', 'Filiere')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')
    filiere = Filiere.objects.create(nom="Physique")
    niveau = Niveau.objects.create(nom="Master 2")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=101, filiere=filiere)
    assert classe.filiere == filiere
    assert classe.niveau == niveau


@pytest.mark.django_db
def test_cascade_delete_filiere_and_classe():
    """
    Teste que la suppression d'une Filiere supprime les Classes associées.
    """
    Filiere = apps.get_model('school', 'Filiere')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')
    filiere = Filiere.objects.create(nom="Chimie")
    niveau = Niveau.objects.create(nom="Master 3")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=102, filiere=filiere)
    filiere.delete()
    assert Classe.objects.filter(id=classe.id).count() == 0


@pytest.mark.django_db
def test_filiere_creation_invalid():
    """
    Teste la création d'une Filiere avec un nom vide.
    """
    Filiere = apps.get_model('school', 'Filiere')
    with pytest.raises(Exception):
        Filiere.objects.create(nom=None)


@pytest.mark.django_db
def test_chapitre_creation():
    """
    Teste la création d'un Chapitre avec un slug valide.
    """
    Matiere = apps.get_model('school', 'Matiere')
    Classe = apps.get_model('school', 'Classe')
    Chapitre = apps.get_model('school', 'Chapitre')
    matiere = Matiere.objects.create(nom="Mathématiques")
    classe = Classe.objects.create(numeroClasse=1)
    chapitre = Chapitre.objects.create(titre="Introduction aux Matrices", matiere=matiere, classe=classe)
    assert str(chapitre) == "Introduction aux Matrices"
    assert chapitre.slug.startswith("introduction-aux-matrices")


@pytest.mark.django_db
def test_matiere_instructor_relation():
    """
    Teste la relation Many-to-Many entre Matiere et Instructor.
    """
    Matiere = apps.get_model('school', 'Matiere')
    Instructor = apps.get_model('instructor', 'Instructor')
    User = apps.get_model('auth', 'User')  # Si le modèle `Instructor` dépend d'un utilisateur.
    user = User.objects.create(username="einstein", password="testpass")
    instructor = Instructor.objects.create(user=user)  # Assurez-vous de créer les champs nécessaires.
    matiere = Matiere.objects.create(nom="Mathématiques")
    matiere.instructor.add(instructor)
    assert instructor in matiere.instructor.all()


@pytest.mark.django_db
def test_islogin_failure():
    """
    Teste si une tentative de connexion avec des identifiants incorrects échoue.
    """
    client = Client()
    data = {
        "username": "wronguser",
        "password": "wrongpass"
    }
    response = client.post(reverse('post'), data, content_type="application/json")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is False
    assert response_data["message"] == "Une erreur s'est produite"


@pytest.mark.django_db
def test_chapitre_creation():
    """
    Teste la création d'un Chapitre avec un slug valide.
    """
    Matiere = apps.get_model('school', 'Matiere')
    Classe = apps.get_model('school', 'Classe')
    Chapitre = apps.get_model('school', 'Chapitre')
    Niveau = apps.get_model('school', 'Niveau')

    niveau = Niveau.objects.create(nom="Licence 3")
    matiere = Matiere.objects.create(nom="Mathématiques")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=1)

    chapitre = Chapitre.objects.create(
        titre="Introduction aux Matrices",
        matiere=matiere,
        classe=classe
    )
    assert str(chapitre) == "Introduction aux Matrices"
    assert chapitre.slug.startswith("introduction-aux-matrices")


@pytest.mark.django_db
def test_cours_creation():
    """
    Teste la création d'un Cours avec un Chapitre associé.
    """
    Matiere = apps.get_model('school', 'Matiere')
    Chapitre = apps.get_model('school', 'Chapitre')
    Cours = apps.get_model('school', 'Cours')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')

    niveau = Niveau.objects.create(nom="Master 1")
    matiere = Matiere.objects.create(nom="Physique Quantique")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=1)

    chapitre = Chapitre.objects.create(
        titre="Chapitre 1",
        matiere=matiere,
        classe=classe
    )
    cours = Cours.objects.create(titre="Cours 1 - Les bases", chapitre=chapitre)
    assert str(cours) == "Cours 1 - Les bases"
    assert cours.chapitre == chapitre
