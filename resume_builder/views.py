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
# Create your views here.


def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')  
        passw = make_password(password)
        user = NewUser.objects.create(first_name=first_name,last_name=last_name,password=passw,email=email,
                       phone_no=contact_no,)
        success_message = f"Registered successfully!"
        return redirect('login_view')

    return render(request, 'registration.html')


def login_view(request):
    id=request.user.id
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            i = request.user.id
            return redirect('Templates')

    return render(request, 'login.html')