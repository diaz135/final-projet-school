from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from school import models as school_models
from forum import models as forum_models
from instructor import models as instructor_models
from django.db.models import Q
from chat import models as chat_models
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from . import models
from quiz.models import Quiz, Devoir, Reponse, Question, QuestionResponse, QuizResult
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        try:
            print("1")
            if request.user.instructor:
                return redirect('dashboard')
        except Exception as e:
            print(e)
            print("2")
            if request.user.student_user:
                datas = {
                }
            return render(request,'pages/fixed-student-dashboard.html',datas)


@login_required(login_url='login')
def payment(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-account-billing-payment-information.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def subscription(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-account-billing-subscription.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def upgrade(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-account-billing-upgrade.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def edit(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-account-edit.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def edit_basic(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-account-edit-basic.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def edit_profile(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-account-edit-profile.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def billing(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-billing.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")

# @login_required(login_url = 'login')
# def browse_courses(request):
#     if request.user.is_authenticated:
#         try:
#             try:
#                 print("1")
#                 if request.user.instructor:
#                     return redirect('dashboard')
#             except Exception as e:
#                 print(e)
#                 print("2")
#                 if request.user.student_user:
#                     cours = school_models.Cours.objects.filter(Q(status=True) & Q(chapitre__classe=request.user.student_user.classe))
#                     datas = {
#                                 'all_cours' : all_cours ,
#                            }
#                 return render(request,'pages/fixed-student-browse-courses.html',datas)
#         except Exception as e:
#             print(e)
#             print("3")
#             return redirect("/admin/")


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-cart.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def courses(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:

                    datas = {

                    }
                return render(request,'pages/fixed-student-courses.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def dashboard(request):
    try:
        if hasattr(request.user, 'instructor'):
            return render(request, 'pages/instructor-dashboard.html', {})
        elif hasattr(request.user, 'student_user'):
            datas = {}
            return render(request, 'pages/fixed-student-dashboard.html', datas)
        else:
            return redirect('/admin/')  # Redirection par défaut
    except Exception as e:
        print(f"Erreur dans dashboard: {e}")
        return redirect('/admin/')


@login_required(login_url='login')
def earnings(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-earnings.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def forum(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    forum_general = forum_models.Sujet.objects.filter(cours=None)
                    forum = forum_models.Sujet.objects.filter(cours_chapitre_classe=request.user.student_user.classe)
                    datas = {
                        'forum_general': forum_general,
                        'forum': forum,
                    }
                return render(request,'pages/fixed-student-forum.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def forum_lesson(request, slug):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    lesson = school_models.Cours.objects.get(slug=slug)
                    datas = {
                        'lesson':lesson,
                    }
                return render(request,'pages/fixed-student-forum-lesson.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def forum_ask(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-forum-ask.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def forum_thread(request, slug):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    forum = forum_models.Sujet.objects.get(slug=slug)
                    datas = {
                        "forum": forum,
                    }
                return render(request,'pages/fixed-student-forum-thread.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def help_center(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-help-center.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def invoice(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-invoice.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def messages(request, classe):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    exist_classe = chat_models.Salon.objects.get(classe=request.user.student_user.classe)
                    info = school_models.Classe.objects.get(id=request.user.student_user.classe.id)
                    instructor = instructor_models.Instructor.objects.get(
                        classe__id=request.user.student_user.classe.id)
                    user_room = ''
                    print(user_room)
                    datas = {
                        'instructor':instructor,
                        'info_classe':info,
                        'classe': exist_classe,
                        'classe_json': mark_safe(json.dumps(exist_classe.id)),
                        'username': mark_safe(json.dumps(request.user.username))
                    }
                return render(request,'pages/fixed-student-messages.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")

# @login_required(login_url = 'login')
# def messages_2(request):
#     if request.user.is_authenticated:
#         try:
#             try:
#                 print("1")
#                 if request.user.instructor:
#                     return redirect('dashboard')
#             except Exception as e:
#                 print(e)
#                 print("2")
#                 if request.user.student_user:
#                     datas = {

#                            }
#                 return render(request,'pages/fixed-student-messages-2.html',datas)
#         except Exception as e:
#             print(e)
#             print("3")
#             return redirect("/admin/")


@login_required(login_url='login')
def my_courses(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    chapitre = school_models.Chapitre.objects.filter(status=True)
                    cours = school_models.Cours.objects.filter(status=True)
                    all_cours = school_models.Cours.objects.filter(
                        Q(status=True) & Q(chapitre__classe=request.user.student_user.classe))
                    datas = {
                        'chapitre':chapitre,
                        'cours':cours,
                        'all_cours': all_cours,
                    }
                return render(request,'pages/fixed-student-my-courses.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@login_required(login_url='login')
def quiz_list(request):
    try:
        if hasattr(request.user, 'instructor'):
            messages.warning(request, "Les instructeurs n'ont pas accès à cette page.")
            return redirect('dashboard')

        if hasattr(request.user, 'student_user'):
            quizzes = Quiz.objects.filter(status=True).select_related('cours')
            devoirs = Devoir.objects.filter(status=True).select_related('chapitre')

            items = []
            for quiz in quizzes:
                items.append({
                    "type": "Quiz",
                    "title": quiz.titre,
                    "date": quiz.date,
                    "slug": quiz.slug,
                    "cours": quiz.cours.titre,
                    "temps": f"{quiz.temps} minutes",
                    "status": "En cours" if quiz.status else "Terminé"
                })

            for devoir in devoirs:
                items.append({
                    "type": "Devoir",
                    "title": devoir.sujet,
                    "date": devoir.dateDebut.strftime("%Y-%m-%d %H:%M"),
                    "slug": devoir.slug,
                    "chapitre": devoir.chapitre.titre,
                    "deadline": devoir.dateFermeture.strftime("%Y-%m-%d %H:%M"),
                    "coefficient": devoir.coefficient
                })

            items.sort(key=lambda x: x['date'], reverse=True)

            context = {
                "items": items,
                "total_quiz": len([item for item in items if item['type'] == 'Quiz']),
                "total_devoirs": len([item for item in items if item['type'] == 'Devoir'])
            }
            return render(request, 'pages/fixed-student-quiz-list.html', context)

        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('login')

    except Exception as e:
        print(f"Erreur dans quiz_list: {str(e)}")
        messages.error(request, "Une erreur est survenue. Veuillez réessayer plus tard.")
        return redirect('index_student')


@login_required(login_url='login')
def take_quiz(request, slug):
    try:
        if hasattr(request.user, 'instructor'):
            return redirect('dashboard')

        if hasattr(request.user, 'student_user'):
            quiz = get_object_or_404(Quiz.objects.select_related('cours'),
                                     slug=slug, status=True)

            questions = quiz.quiz_question.filter(
                status=True
            ).prefetch_related(
                'question_reponse'
            ).order_by('?')

            if not quiz.status:
                return redirect('quiz-list')

            data = {
                'quiz': quiz,
                'questions': questions,
                'total_questions': questions.count(),
                'temps_restant': quiz.temps * 60,
                'cours': quiz.cours
            }

            return render(request, 'pages/fixed-student-take-quiz.html', data)

        return redirect('login')

    except Exception as e:
        print(f"Erreur dans take_quiz: {str(e)}")
        return redirect('quiz-list')


@login_required(login_url='login')
def take_devoir(request, slug):
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'student_user'):
                devoir = get_object_or_404(Devoir, slug=slug, status=True)
                data = {
                    'devoir': devoir,
                }
                return render(request, 'pages/fixed-student-take-devoir.html', data)
            return redirect('dashboard')
        except Exception as e:
            print(e)
            return redirect('quiz-list')

# @login_required(login_url = 'login')
# def quiz_list(request):
#     if request.user.is_authenticated:
#         try:
#             try:
#                 print("1")
#                 if request.user.instructor:
#                     return redirect('dashboard')
#             except Exception as e:
#                 print(e)
#                 print("2")
#                 if request.user.student_user:
#                     datas = {

#                            }
#                 return render(request,'pages/fixed-student-quiz-list.html',datas)
#         except Exception as e:
#             print(e)
#             print("3")
#             return redirect("/admin/")


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# //////////////////////////////////////////////////////////////////


@login_required(login_url='login')
def submit_quiz(request, quiz_slug):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

    try:
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        data = json.loads(request.body)
        answers = data.get('answers', {})
        time_taken = data.get('timeTaken', 0)

        total_questions = quiz.quiz_question.count()
        correct_answers = 0

        # Créer un résultat pour le quiz
        quiz_result = QuizResult.objects.create(
            student=request.user,
            quiz=quiz,
            total_questions=total_questions,
            completion_time=time_taken
        )

        for question_id, selected_answers in answers.items():
            question = Question.objects.get(id=question_id)
            correct_answer_ids = list(question.question_reponse.filter(is_True=True).values_list('id', flat=True))
            is_correct = sorted(map(int, selected_answers)) == sorted(correct_answer_ids)

            if is_correct:
                correct_answers += 1

            # Enregistrer la réponse
            QuestionResponse.objects.create(
                quiz_result=quiz_result,
                question=question,
                selected_answer=','.join(map(str, selected_answers)),
                is_correct=is_correct
            )

        # Calculer le score
        score = (correct_answers / total_questions) * 100
        quiz_result.score = score
        quiz_result.correct_answers = correct_answers
        quiz_result.save()

        # Retourner l'ID du résultat pour redirection
        return JsonResponse({
            'success': True,
            'redirect_url': f"{request.build_absolute_uri('/')[:-1]}{quiz_result.get_absolute_url()}"
        })

    except Exception as e:
        print(f"Erreur dans submit_quiz: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required(login_url='login')
def quiz_results(request, result_id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        if result_id:
            quiz_result = get_object_or_404(QuizResult, id=result_id, student=request.user)
            question_responses = quiz_result.question_responses.all().select_related('question')
            data = {
                'result': quiz_result,
                'responses': question_responses,
                'completion_time_minutes': quiz_result.completion_time // 60,
                'completion_time_seconds': quiz_result.completion_time % 60,
            }
        else:
            results = QuizResult.objects.filter(student=request.user).select_related('quiz').order_by('-completed_at')
            data = {
                'results': results,
            }

        return render(request, 'pages/fixed-student-quiz-results.html', data)

    except Exception as e:
        print(f"Erreur dans quiz_results: {str(e)}")
        return redirect('index_student')


@login_required(login_url='login')
def my_quiz_results(request):
    if request.user.is_authenticated:
        try:
            results = QuizResult.objects.filter(
                student=request.user
            ).select_related('quiz').order_by('-completed_at')

            context = {
                'results': results
            }
            return render(request, 'pages/fixed-student-my-results.html', context)

        except Exception as e:
            print(f"Error in my_quiz_results: {str(e)}")
            return redirect('quiz-list')


# //////////////////////////////////////////////////////////////////


@login_required(login_url='login')
def profile(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-profile.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def profile_posts(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-profile-posts.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def quiz_results(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-quiz-results.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def quizzes(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-quizzes.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def statement(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-statement.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


# @login_required(login_url = 'login')
# def student_take_course(request, slug):
#     if request.user.is_authenticated:
#         try:
#             try:
#                 print("1")
#                 if request.user.instructor:
#                     return redirect('dashboard')
#             except Exception as e:
#                 print(e)
#                 print("2")
#                 if request.user.student_user:
#                     cours  = school_models.Cours.objets.get(slug=slug)
#                     datas = {
#                         'cours': cours,
#                     }
#                 return render(request,'pages/fixed-student-student-take-course.html',datas)
#         except Exception as e:
#             print(e)
#             print("3")
#             return redirect("/admin/")


@login_required(login_url='login')
def take_course(request, slug):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    cours = school_models.Cours.objects.get(slug=slug)
                    instructor = instructor_models.Instructor.objects.get(
                        classe__id=request.user.student_user.classe.id)
                    datas = {
                        'cours': cours,
                        'instructor': instructor,
                    }
                return render(request,'pages/fixed-student-take-course.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect('my_courses')


@login_required(login_url='login')
def take_quiz(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-take-quiz.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def view_course(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-view-course.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


@login_required(login_url='login')
def account_edit(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                    }
                return render(request,'pages/fixed-student-account-edit.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


def update_profil(request):
    nom = request.POST.get("nom")
    prenom = request.POST.get("prenom")
    email = request.POST.get("email")
    bio = request.POST.get("bio")

    try:
        user = User.objects.get(username=request.user.username)
        user.last_name = nom
        user.first_name = prenom
        user.email = email
        user.save()
        student = models.Student.objects.get(user__id=request.user.id)
        student.bio = bio
        student.save()
        try:
            image = request.FILES["file"]
            student.photo = image
            student.save()

        except BaseException:
            pass
        success = True
        message = "vos informations ont été modifié avec succés"

    except BaseException:
        success = False
        message = "une erreur est subvenue lors de la mise à jour"
    data = {
        "success": success,
        "message": message,
    }
    return JsonResponse(data,safe=False)


def update_password(request):
    last_password = request.POST.get("last_password")
    new_password = request.POST.get("new_password")
    confirm_password = request.POST.get("confirm_password")

    try:
        if not request.user.check_password(last_password):
            success = False
            message = "Ancien mot de passe incorrect"
        elif new_password != confirm_password:
            success = False
            message = "Les mots de passe ne sont pas identiques"
        else:
            user = User.objects.get(username=request.user.username)
            username = user.username
            user.password = new_password
            user.set_password(user.password)
            user.save()
            user = authenticate(username=username, password=new_password)
            login(request, user)
            success = True
            message = "Mot de passe modfifié avec succès"
    except Exception as e:
        print(e)
        success = False
        message = "une erreur est subvenue lors de la mise à jour"
    data = {
        "success": success,
        "message": message,
    }
    return JsonResponse(data,safe=False)


def post_forum(request):
    titre = request.POST.get("titre")
    question = request.POST.get("question")
    lesson = request.POST.get("lesson")
    val = ""
    try:
        lesson = school_models.Cours.objects.get(id=int(lesson))
        forum = forum_models.Sujet()
        forum.titre = titre
        forum.question = question
        forum.cours = lesson
        forum.user = request.user
        forum.save()
        val = forum.slug
        success = True
        message = "Votre sujet a bien été ajouté!"
    except Exception as e:
        print(e)
        success = False
        message = "une erreur est subvenue lors de la soumission"
    data = {
        "success": success,
        "message": message,
        "forum": val,
    }
    return JsonResponse(data,safe=False)


def post_forum_g(request):
    titre = request.POST.get("titre")
    question = request.POST.get("question")
    val = ""
    try:
        forum = forum_models.Sujet()
        forum.titre = titre
        forum.question = question
        forum.user = request.user
        forum.save()
        val = forum.slug
        success = True
        message = "Votre sujet a bien été ajouté!"
    except Exception as e:
        print(e)
        success = False
        message = "une erreur est subvenue lors de la soumission"
    data = {
        "success": success,
        "message": message,
        "forum": val,
    }
    return JsonResponse(data,safe=False)
