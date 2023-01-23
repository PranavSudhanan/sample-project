import uuid

from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.core.mail import send_mail
from Email_Project.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate


# Create your views here.

def register(request):
    a = regform()
    return render(request, 'register.html', {'form':a})

def contact(request):
    a = contactform()
    if request.method=='POST':
        b = contactform(request.POST)
        if b.is_valid():
            nm = b.cleaned_data['name']
            em = b.cleaned_data['email']
            ms = b.cleaned_data['message']
            send_mail(str(nm)+"||"+"TCS", ms, EMAIL_HOST_USER, [em])
    #         send_mail(subject, message, EMAIL_HOST_USER, [EMAIL])
            return render(request, 'success.html')
    return render(request, 'contact.html', {'form':a})


def reg(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).first():
# .first : it will get the first object from the filter query
            messages.success(request, 'username already taken')
            return redirect(reg)
        if User.objects.filter(email=email).first():
            messages.success(request, 'email already exist')
            return redirect(reg)

        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()

        auth_token = str(uuid.uuid4())

        profile_obj = profile.objects.create(user=user_obj, auth_token=auth_token)
        profile_obj.save()

        send_mail_regis(email, auth_token)
        return render(request, 'success.html')
    return render(request, 'registration.html')

def send_mail_regis(email, auth_token):
    subject = "Your Account has been Verified"
    message = f'Paste the link to verify your account http://127.0.0.1:8000/EmailApp/verify/{auth_token}'
    email_from = EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject, message, email_from, recipient)


def verify(request, auth_token):
    profile_obj = profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'Your account is already verified')
            return redirect(login)
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, 'Your account has been verified')
        return redirect(login)
    else:
        messages.success(request, "User not found")
        return redirect(login)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found')
            return redirect(login)
        profile_obj = profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Profile not verified, Check your mail')
            return redirect(login)
        user = authenticate(username=username,password=password)
        if user is None:
            messages.success(request, 'Wrong username or password')
            return redirect(login)
        return HttpResponse("Success")
    return render(request, 'login.html')
