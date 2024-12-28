import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.apps import apps
import json
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.apps import apps


# UNIT TESTS
@pytest.mark.django_db
def test_student_creation():
    """
    Teste la création d'un Student avec un utilisateur et une classe associés.
    """
    User = apps.get_model('auth', 'User')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')
    Student = apps.get_model('student', 'Student')

    niveau = Niveau.objects.create(nom="Licence 1")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=1)
    user = User.objects.create_user(username="etudiant", password="testpass")

    student = Student.objects.create(
        user=user,
        classe=classe,
        bio="Étudiant passionné."
    )
    assert str(student) == "etudiant"
    assert student.classe == classe
    assert student.bio == "Étudiant passionné."


@pytest.mark.django_db
def test_student_missing_user():
    """
    Teste la création d'un Student sans utilisateur (doit échouer).
    """
    Student = apps.get_model('student', 'Student')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')

    niveau = Niveau.objects.create(nom="Licence 2")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=2)

    with pytest.raises(Exception):
        Student.objects.create(
            classe=classe,
            bio="Erreur prévue."
        )

# FUNCTIONAL TESTS


@pytest.mark.django_db
def test_index_view_student():
    """
    Vérifie que la vue `index` redirige correctement les utilisateurs basés sur leur rôle.
    """
    User = apps.get_model('auth', 'User')
    Student = apps.get_model('student', 'Student')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')

    niveau = Niveau.objects.create(nom="Licence 2")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=1)
    user = User.objects.create_user(username="etudiant", password="testpass")
    Student.objects.create(user=user, classe=classe)

    client = Client()
    client.login(username="etudiant", password="testpass")
    response = client.get(reverse('index_student'))

    assert response.status_code == 200
    assert 'fixed-student-dashboard.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_courses_view_student():
    """
    Teste l'affichage des cours disponibles pour un étudiant.
    """
    User = apps.get_model('auth', 'User')
    Student = apps.get_model('student', 'Student')
    Classe = apps.get_model('school', 'Classe')
    Niveau = apps.get_model('school', 'Niveau')
    Cours = apps.get_model('school', 'Cours')

    niveau = Niveau.objects.create(nom="Licence 1")
    classe = Classe.objects.create(niveau=niveau, numeroClasse=1)
    user = User.objects.create_user(username="etudiant", password="testpass")
    student = Student.objects.create(user=user, classe=classe)

    chapitre = apps.get_model('school', 'Chapitre').objects.create(titre="Introduction", classe=classe)
    cours = Cours.objects.create(titre="Cours 1", chapitre=chapitre)

    client = Client()
    client.login(username="etudiant", password="testpass")
    response = client.get(reverse('courses'))

    assert response.status_code == 200
    assert cours in response.context['all_cours']

# INTEGRATION TESTS


@pytest.mark.django_db
def test_take_quiz_view():
    """
    Teste la tentative d'un quiz par un étudiant.
    """
    User = apps.get_model('auth', 'User')
    Student = apps.get_model('student', 'Student')
    Quiz = apps.get_model('quiz', 'Quiz')
    Question = apps.get_model('quiz', 'Question')

    user = User.objects.create_user(username="etudiant", password="testpass")
    student = Student.objects.create(user=user)
    quiz = Quiz.objects.create(titre="Quiz Mathématiques", temps=30, status=True)
    question = Question.objects.create(quiz=quiz, titre="2+2")

    client = Client()
    client.login(username="etudiant", password="testpass")
    response = client.get(reverse('take_quiz', kwargs={'slug': quiz.slug}))

    assert response.status_code == 200
    assert response.context['quiz'] == quiz
    assert response.context['total_questions'] == quiz.quiz_question.count()


@pytest.mark.django_db
def test_submit_quiz():
    """
    Teste la soumission d'un quiz par un étudiant.
    """
    User = apps.get_model('auth', 'User')
    Student = apps.get_model('student', 'Student')
    Quiz = apps.get_model('quiz', 'Quiz')
    Question = apps.get_model('quiz', 'Question')
    QuizResult = apps.get_model('quiz', 'QuizResult')

    user = User.objects.create_user(username="etudiant", password="testpass")
    student = Student.objects.create(user=user)
    quiz = Quiz.objects.create(titre="Quiz Mathématiques", temps=30, status=True)
    question = Question.objects.create(quiz=quiz, titre="2+2")

    client = Client()
    client.login(username="etudiant", password="testpass")
    data = {
        "answers": {str(question.id): ["4"]},
        "timeTaken": 120
    }
    response = client.post(
        reverse(
            'submit_quiz',
            kwargs={
                'quiz_slug': quiz.slug}),
        data=json.dumps(data),
        content_type="application/json")

    assert response.status_code == 200
    assert QuizResult.objects.filter(student=student, quiz=quiz).exists()


@pytest.mark.django_db
def test_quiz_results_view():
    """
    Teste l'affichage des résultats des quiz pour un étudiant.
    """
    User = apps.get_model('auth', 'User')
    Student = apps.get_model('student', 'Student')
    Quiz = apps.get_model('quiz', 'Quiz')
    QuizResult = apps.get_model('quiz', 'QuizResult')

    user = User.objects.create_user(username="etudiant", password="testpass")
    student = Student.objects.create(user=user)
    quiz = Quiz.objects.create(titre="Quiz Mathématiques", temps=30, status=True)
    result = QuizResult.objects.create(student=student, quiz=quiz, score=85)

    client = Client()
    client.login(username="etudiant", password="testpass")
    response = client.get(reverse('quiz_results', kwargs={'result_id': result.id}))

    assert response.status_code == 200
    assert response.context['result'] == result
