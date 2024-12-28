from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('account_edit', views.account_edit, name='instructor-account-edit'),
    path('course_edit/<slug>', views.course_edit, name='course-edit'),
    path('course_add', views.course_add, name='course-add'),
    path('courses', views.courses, name='instructor-courses'),
    path('matiere/<slug>', views.matiere, name='instructor-matiere'),
    path('forum', views.forum, name='instructor-forum'),
    path('forum_ask', views.forum_ask, name='instructor-forum-ask'),
    path('forum_thread/<slug>', views.forum_thread, name='instructor-forum-thread'),
    path('lesson-add/<slug>', views.lesson_add, name='instructor-lesson-add'),
    path('lesson-edit/<id>/<slug>', views.lesson_edit, name='instructor-lesson-edit'),
    path('messages/<str:classe>/', views.messages, name='instructor-messages'),
    path('profile', views.profile, name='instructor-profile'),
    path('quiz_edit/<int:quiz_id>/', views.quiz_edit, name='instructor-quiz-edit'),
    path('quiz_add/', views.quiz_add, name='instructor-quiz-add'),
    path('review_quiz', views.review_quiz, name='instructor-review-quiz'),
    path('quizzes', views.quizzes, name='instructor-quizzes'),
    path('add_question/<int:quiz_id>/', views.add_question, name='instructor-add_question'),


    # post url
    path('post_cours',views.post_cours,name='post_cours'),
    path('delete_chapitre',views.delete_chapitre,name='delete_chapitre'),
    path('delete_lesson',views.delete_lesson,name='delete_lesson'),
    path('post_lesson',views.post_lesson,name='post_lesson'),


    ########## post ###############
    path('update_profil', views.update_profil, name='update_profil'),
    path('update_password', views.update_password, name='update_password'),
    path('post_forum', views.post_forum, name='instructor_post_forum'),

]
