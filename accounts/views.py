from random import randint, random
from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

global otp 
global user 
from django.http import HttpResponseRedirect

@login_required
def home(request):
    return render(request , 'accounts/home.html')



def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first() 

        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first() 


        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')
        global user 
        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')
        email = User.objects.filter(username = username).values_list('email',flat=True)
        email = list(email)[0]  
        global otp
        otp = randint(1000,9999)
        send_otp_for_login(email, otp)  
        print("user is " , user)
        return render(request, 'accounts/otp_check.html', {'user':user}) 
        
        # login(request , user)
        # return redirect('/')

    return render(request , 'accounts/login.html')

def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'accounts/register.html')

def success(request):
    return render(request , 'accounts/success.html')


def token_send(request):
    return render(request , 'accounts/token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'accounts/error.html')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    
def send_otp_for_login(email , otp): 
    subject = 'for login use this otp'
    message = f'{otp} is your otp'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list ) 
    

# def verify_otp(request,user):
def verify_otp(request):
    if request.method == "POST":
        global user 
        otp_rec = request.POST.get('otp')
        if int(otp_rec)== otp:
            print("vvvverified ")
            login(request , user)
            return redirect('/')
        else:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'accounts/otp_check.html')

            



