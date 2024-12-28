import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

# TESTS UNITAIRES


@pytest.mark.django_db
def test_create_quiz_with_valid_data():
    """
    Teste la création d'un quiz avec des données valides.
    """
    Quiz = apps.get_model('quiz', 'Quiz')
    quiz = Quiz.objects.create(
        titre="Quiz Mathématiques",
        temps=20,
        status=True
    )
    assert Quiz.objects.count() == 1
    assert quiz.titre == "Quiz Mathématiques"
    assert quiz.status is True


@pytest.mark.django_db
def test_question_creation_without_score():
    """
    Vérifie qu'une question ne peut pas être créée sans un score valide.
    """
    Question = apps.get_model('quiz', 'Question')
    with pytest.raises(Exception):
        Question.objects.create(
            title="Question sans score",
            question_type="Text",
            score=None,  # Champ manquant
            status=True
        )


@pytest.mark.django_db
def test_delete_quiz_with_dependencies():
    """
    Vérifie que la suppression d'un quiz supprime aussi les questions et réponses associées.
    """
    Quiz = apps.get_model('quiz', 'Quiz')
    Question = apps.get_model('quiz', 'Question')
    Reponse = apps.get_model('quiz', 'Reponse')

    quiz = Quiz.objects.create(titre="Quiz à supprimer", temps=15, status=True)
    question = Question.objects.create(
        title="Question associée",
        quiz=quiz,
        question_type="Text",
        score=10,
        status=True
    )
    Reponse.objects.create(reponse="Réponse associée", question=question, is_True=True)

    quiz.delete()
    assert Quiz.objects.count() == 0
    assert Question.objects.count() == 0
    assert Reponse.objects.count() == 0

# TESTS FONCTIONNELS


@pytest.mark.django_db
def test_list_quiz_view():
    """
    Vérifie que la liste des quiz est accessible via l'interface utilisateur.
    """
    User = apps.get_model('auth', 'User')
    Quiz = apps.get_model('quiz', 'Quiz')

    user = User.objects.create_user(username="user_test", password="password")
    Quiz.objects.create(titre="Quiz de test", temps=10, status=True)

    client = Client()
    client.login(username="user_test", password="password")

    response = client.get(reverse('quiz_list'))
    assert response.status_code == 200
    assert "Quiz de test" in str(response.content)


@pytest.mark.django_db
def test_view_questions_in_quiz():
    """
    Vérifie que les questions associées à un quiz sont correctement affichées.
    """
    User = apps.get_model('auth', 'User')
    Quiz = apps.get_model('quiz', 'Quiz')
    Question = apps.get_model('quiz', 'Question')

    user = User.objects.create_user(username="user_test", password="password")
    quiz = Quiz.objects.create(titre="Quiz Science", temps=20, status=True)
    Question.objects.create(
        title="Quelle est la vitesse de la lumière ?",
        quiz=quiz,
        question_type="Text",
        score=10,
        status=True
    )

    client = Client()
    client.login(username="user_test", password="password")

    response = client.get(reverse('quiz_detail', args=[quiz.id]))
    assert response.status_code == 200
    assert "Quelle est la vitesse de la lumière ?" in str(response.content)

# TESTS D'INTÉGRATION


@pytest.mark.django_db
def test_complete_quiz_flow():
    """
    Vérifie le flux complet : création d'un quiz, ajout de questions et réponses, et affichage.
    """
    User = apps.get_model('auth', 'User')
    Quiz = apps.get_model('quiz', 'Quiz')
    Question = apps.get_model('quiz', 'Question')
    Reponse = apps.get_model('quiz', 'Reponse')

    user = User.objects.create_user(username="instructor_test", password="password")
    quiz = Quiz.objects.create(titre="Quiz Intégration", temps=30, status=True)

    question = Question.objects.create(
        title="Quelle est la capitale de la France ?",
        quiz=quiz,
        question_type="Text",
        score=5,
        status=True
    )
    Reponse.objects.create(reponse="Paris", question=question, is_True=True)
    Reponse.objects.create(reponse="Londres", question=question, is_True=False)

    client = Client()
    client.login(username="instructor_test", password="password")

    # Vérification de l'affichage du quiz
    response = client.get(reverse('quiz_detail', args=[quiz.id]))
    assert response.status_code == 200
    assert "Quelle est la capitale de la France ?" in str(response.content)
    assert "Paris" in str(response.content)
    assert "Londres" in str(response.content)


@pytest.mark.django_db
def test_invalid_quiz_submission():
    """
    Vérifie que la soumission d'un quiz échoue si le temps est dépassé.
    """
    User = apps.get_model('auth', 'User')
    Quiz = apps.get_model('quiz', 'Quiz')

    user = User.objects.create_user(username="user_quiz", password="password")
    quiz = Quiz.objects.create(titre="Quiz Temps Limité", temps=5, status=True)

    client = Client()
    client.login(username="user_quiz", password="password")

    data = {
        "answers": {"1": ["2"]},  # Réponses fictives
        "timeTaken": 600  # Temps dépassé (600 secondes)
    }
    response = client.post(reverse('quiz_submit', args=[quiz.slug]), data, content_type="application/json")
    assert response.status_code == 400
    assert "Temps dépassé" in str(response.content)
