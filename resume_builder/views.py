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
from .models import  NewUser,Header,User_skills,Experience,Education,TemplatesInfo
from datetime import datetime
# Create your views here.

def add_template(request):
    if request.method == 'POST':
        view_name = request.POST.get('view_name')
        image = request.FILES.get('image')

        # Create a new MyModel instance and save the form data
        my_model_instance = TemplatesInfo(view_name=view_name, template_image=image)
        my_model_instance.save()

        # Redirect to a new URL (change as needed)
        return redirect('/add_template')

    # Render the form template for GET requests
    return render(request, 'add_template.html')


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
            return redirect('/resumes')
        else:
           
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'login.html')
    

def index(request):
    return render(request,'index.html')


def resumes(request):
    templates = TemplatesInfo.objects.all()
    context = {
        'templates':templates
    }
    return render(request,'resumes.html', context)

def add_experience_choice(request):
    return render(request,'add_experience_choice.html')

def add_education_choice(request):
    return render(request,'add_education_choice.html')

def resume_options(request):
    return render(request,'resume_options.html')


def personal_info(request, id):
    request.session['template_id'] = id
    temp_image = TemplatesInfo.objects.get(id=id)
    print(temp_image.template_image)
    t_image = temp_image.template_image
    id=request.user.id
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        linkedin = request.POST.get('linkedin')
        summary = request.POST.get('summary')
        skills=request.POST.get('skills')
        user=Header.objects.create(first_name=first_name,last_name=last_name,email=email,
                              contact_no=contact_no,linkedin_url=linkedin,summary=summary,user_id_id=id)
        data=User_skills.objects.create(skills=skills,user_id_id=id)
        if user:
            return redirect('work_history')
    context = {
        't_image':t_image
    }
    return render(request,'personal_info.html',context)


def work_history(request):
    id = request.user.id
    if request.method == 'POST':
        designation = request.POST.get('designation')
        company_name = request.POST.get('company_name')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        description = request.POST.get('description')
        
        if 'to_present' in request.POST:
            # If "To Present" checkbox is checked, set to_date to the current date
            to_date ='Present'  # Format to match your field type
            
        data = Experience.objects.create(designation=designation, company_name=company_name, from_date=from_date,
                                         to_date=to_date, description=description, user_id_id=id)
        if data:
            return redirect('add_experience_choice')
    return render(request, 'work_history.html')

def education(request):
    id = request.user.id
    if request.method == 'POST':
        college_name = request.POST.get('college_name')
        degree = request.POST.get('degree')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        city = request.POST.get('city')
        cgpa = request.POST.get('cgpa')
        data=Education.objects.create(college_name=college_name,degree=degree,from_date=from_date,
                                      to_date=to_date,city=city,cgpa=cgpa,user_id_id=id)
        if data:
            return redirect('add_education_choice')
    return render(request,'education.html')

def extra_details(request):
    return render(request,'extra_details.html')

def template1(request):
    user_id = request.user.id
    print("!!!!!!!!!!!!1",user_id)
    template_id = request.session.get('template_id')
    print(template_id)
    data = TemplatesInfo.objects.get(id=template_id)
    template_html_id = data.id_name
    print(template_html_id)
    print(template_id)

    # fetching header section
    personal_info = Header.objects.get(user_id_id=user_id)

    # fetching exp section
    exp_info = Experience.objects.filter(user_id_id=user_id)
    print("exppppppppppppppppp",exp_info)
    context = {
        'template_html_id':template_html_id,
        'personal_info':personal_info,
        'exp_info':'exp_info',
    }
    return render(request,'template1.html',context)

def set(request):
    return render(request,'set.html')