from django.shortcuts import render
from django.contrib.auth import authenticate, login as login_request, logout
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail  # Pour envoyer un email à l'admin (optionnel)
from django.conf import settings


def demander_creation_compte(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Envoyer un email à l'administrateur (optionnel)
        if settings.EMAIL_HOST:
            send_mail(
                subject=f"Demande de création de compte : {nom}",
                message=f"Nom : {nom}\nEmail : {email}\nMessage : {message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
            )

        messages.success(request, "Votre demande a été envoyée à l'administrateur.")
        return redirect('demander_creation_compte')

    return render(request, 'demander_creation_compte.html')


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.student_user:
                    return redirect('index_student')
            except BaseException:
                print("2")
                if request.user.instructor:
                    return redirect('dashboard')
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    else:
        datas = {

        }
        return render(request, 'pages/guest-login.html', datas)


def signup(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.student_user:
                    return redirect('index_student')
            except BaseException:
                print("2")
                if request.user.instructor:
                    return redirect('dashboard')
        except BaseException:
            print("3")
            return redirect("/admin/")
    else:

        datas = {

        }
        return render(request, 'pages/guest-signup.html', datas)


def forgot_password(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.student_user:
                    return redirect('index_student')
            except BaseException:
                print("2")
                if request.user.instructor:
                    return redirect('dashboard')
        except BaseException:
            print("3")
            return redirect("/admin/")
    else:
        datas = {

        }
        return render(request, 'pages/guest-forgot-password.html', datas)


def islogin(request):

    postdata = json.loads(request.body.decode('utf-8'))

    # name = postdata['name']

    username = postdata['username']
    password = postdata['password']

    isSuccess = False
    u_type = ''
    try:

        if '@' in username:
            user = authenticate(email=username, password=password)
            utilisateur = User.objects.get(email=username)
            print(username)
        else:
            user = authenticate(username=username, password=password)
            utilisateur = User.objects.get(username=username)

        if user is not None and user.is_active:
            print("user is login")
            isSuccess = True
            login_request(request, user)
            try:
                try:
                    print("1")
                    if utilisateur.student_user:
                        u_type = "student"
                except BaseException:
                    print("2")
                    if utilisateur.instructor:
                        u_type = "instructor"
            except BaseException:
                print("3")
                u_type = "admin"

            datas = {
                'redirect': u_type,
                'success':True,
                'message':'Vous êtes connectés!!!',
            }
            return JsonResponse(datas,safe=False)  # page si connect

        else:
            data = {
                'success':False,
                'message':'Vos identifiants ne sont pas correcte',
            }
            return JsonResponse(data, safe=False)
    except BaseException:
        data = {
            'success':False,
            'message':"Une erreur s'est produite",
        }
        return JsonResponse(data, safe=False)


def deconnexion(request):
    logout(request)
    return redirect('login')
