from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseBadRequest
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from .models import  NewUser
# Create your views here.




def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact_no = request.POST.get('phone_no')

        # Check if email is unique
        if NewUser.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error_message': 'Email already exists'})
        if len(contact_no) != 10:
            return render(request, 'registration.html', {'error_message': 'Phone number must be 10 digits'})

        passw = make_password(password)
        user = NewUser.objects.create(username=first_name, last_name=last_name, password=passw, email=email, contact_no=contact_no)

        # Display a success message
        return render(request, 'registration.html', {'success_message': 'Registration successful!'})
        user = NewUser.objects.create(first_name=first_name,last_name=last_name,password=passw,email=email,phone_no=contact_no,)
        success_message = f"Registered successfully!"
        return redirect('login_view')

    return render(request, 'registration.html')
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Templates')
        else:
           
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'login.html')
    return render(request, 'login.html')


def index(request):
    return render(request,'index.html')


def resumes(request):
    return render(request,'resumes.html')

def add_experience_choice(request):
    return render(request,'add_experience_choice.html')

def add_education_choice(request):
    return render(request,'add_education_choice.html')

def resume_options(request):
    return render(request,'resume_options.html')


def personal_info(request):
    return render(request,'personal_info.html')

def work_history(request):
    return render(request,'work_history.html')

def education(request):
    return render(request,'education.html')

def extra_details(request):
    return render(request,'extra_details.html')