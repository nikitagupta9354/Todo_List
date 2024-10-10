from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import User
from Todoist import settings
from django.core.mail import send_mail


# Create your views here.
def email_send(request,email,name):
    subject = 'Thanks '+name+' for registering to our site'
    message = 'Welcome to Todoist!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )
    
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        match = User.objects.filter(email=email).exists()
        if match:
            messages.error(request, "Use different email") 
        else:
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            pward = request.POST.get('password')
            cpward = request.POST.get('confirm_password')
            if pward == cpward:
                user=User.objects.create(first_name=fname,
                                         last_name=lname,
                                         email=email)
                user.set_password(pward)
                user.save()
                email_send(request,email,fname)
                messages.success(request, "Account is created")
                return redirect('login')
            else:
                messages.error(request, "Password & Confirm Password not Matched")
                
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        email= request.POST['email']
        password= request.POST['password']
        user= auth.authenticate(email=email,password= password)
        if user is not None:
            auth.login(request, user)
            return redirect('showTasks')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    return redirect('login')

