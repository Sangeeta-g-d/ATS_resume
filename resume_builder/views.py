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
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # Add this import
from .models import  NewUser,Header,User_skills,Experience,Education,TemplatesInfo,Resume,Extracted_ResumeDetails,Extracted_ExperienceDetails,Extracted_EducationDetails,Project,Certificates,Languages
from .models import  NewUser,Header,User_skills,Experience,Education,TemplatesInfo,Project,Certificates,Languages
from datetime import datetime
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
import requests
from .models import NewUser
from django.conf import settings
import requests
from django.http import HttpResponseForbidden

from django.shortcuts import redirect
from google.auth import credentials
from google.oauth2 import id_token




def google_auth(request):
    # Redirect user to Google login page
    redirect_uri = request.build_absolute_uri('/accounts/google/login/callback/')
    google_oauth2_client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    return redirect(f'https://accounts.google.com/o/oauth2/auth?client_id={google_oauth2_client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email')



def google_auth_callback(request):
    # Handle Google callback
    code = request.GET.get('code')

    # Exchange authorization code for tokens
    token_request_data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': request.build_absolute_uri('/accounts/google/login/callback/'),
        'grant_type': 'authorization_code'
    }

    response = requests.post('https://oauth2.googleapis.com/token', data=token_request_data)
    token_data = response.json()

    # Check if there was an error in retrieving tokens
    if 'error' in token_data:
        error_message = token_data.get('error_description', 'Unknown error')
        print("Error in token exchange:", error_message)
        return redirect('index')

    # Use token to get user information
    if 'access_token' in token_data:
        access_token = token_data['access_token']
        user_info_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', params={'access_token': access_token})

        # Check if there was an error in retrieving user information
        if user_info_response.status_code != 200:
            print("Error in fetching user information from Google:", user_info_response.text)
            return redirect('index')

        user_info = user_info_response.json()

        # Extract relevant user data
        email = user_info.get('email')

        # Check if the user already exists
        user = NewUser.objects.filter(email=email).first()
        if user is None:
            # If the user does not exist, create a new one
            user = NewUser.objects.create_user(email=email,username=email)
            user.save()

        # Authenticate and login the user
        user = authenticate(request, email=email)
        print("llllllllllllllllll",user)
        if user is not None:
            login(request, user)
            return redirect('resumes')

    return redirect('resumes')






def add_template(request):
    if request.method == 'POST':
        view_name = request.POST.get('view_name')
        image = request.FILES.get('image')
        template_id = request.POST.get('template_id')
        template_price = request.POST.get('template_price')
        my_model_instance = TemplatesInfo(view_name=view_name, template_image=image,id_name=template_id, price = template_price)
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
        return redirect('/login')
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

def user_logout(request):
    logout(request)
    # Redirect to a specific page after logout (optional)
    return redirect('/')


@login_required(login_url='/login')
def resumes(request):
    id = request.user.id
    print(id)
    templates = TemplatesInfo.objects.all()
    context = {
        'templates': templates
    }
    return render(request, 'resumes.html', context)

@login_required(login_url='/login')
def add_experience_choice(request):
    user_id=request.user.id
    details=Experience.objects.filter(user_id_id=user_id)
    context={'details':details}
    return render(request,'add_experience_choice.html',context)


@login_required(login_url='/login')
def delete_experience(request, experience_id):
    try:
        # Get the experience object
        experience = Experience.objects.get(id=experience_id)
        # Check if the user owns this experience (optional, depending on your requirements)
        if experience.user_id_id != request.user.id:
            # Return an error or redirect to a page indicating unauthorized access
            pass  # Handle unauthorized access here
        else:
            # Delete the experience
            experience.delete()
    except Experience.DoesNotExist:
        # Handle the case where the experience with the given ID does not exist
        pass  # Handle error gracefully

    # Redirect to a suitable page after deletion
    return redirect('/add_experience_choice')


@login_required(login_url='/login')
def delete_project(request, project_id):
    print("ddddd",project_id)
    try:
        project = Project.objects.get(id=project_id)
        print("pppppppp")
        # Check if the user owns this project (optional, depending on your requirements)
        if project.user_id_id != request.user.id:
            return JsonResponse({'success': False, 'message': 'Unauthorized access'}, status=403)
        else:
            project.delete()
            return JsonResponse({'success': True})
    except Project.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Project not found'}, status=404)

@login_required(login_url='/login')
def delete_education(request, education_id):
    try:
        education = Education.objects.get(id=education_id)
        # Check if the user owns this education entry (optional, depending on your requirements)
        if education.user_id_id != request.user.id:
            return JsonResponse({'success': False, 'message': 'Unauthorized access'}, status=403)
        else:
            education.delete()
            return JsonResponse({'success': True})
    except Education.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Education entry not found'}, status=404)

@login_required(login_url='/login')
def edit_experience_choice(request,id):
    user_id=request.user.id
    details=Experience.objects.filter(user_id_id=user_id)
    context={'details':details,'template_id':id}
    return render(request,'edit_experience_choice.html',context)

@login_required(login_url='/login')
def add_education_choice(request):
    user_id=request.user.id
    details=Education.objects.filter(user_id_id=user_id)
    context={'details':details}
    return render(request,'add_education_choice.html',context)

@login_required(login_url='/login')
def edit_education_choice(request,id):
    user_id=request.user.id
    details=Education.objects.filter(user_id_id=user_id)
    context={'details':details,'template_id':id}
    return render(request,'edit_education_choice.html',context)

@login_required(login_url='/login')
def personal_info(request, id):
    request.session['template_id'] = id
    temp_image = TemplatesInfo.objects.get(id=id)
    print(temp_image.template_image)
    t_image = temp_image.template_image
    user_id=request.user.id
    # check user existance 
    user_obj = Header.objects.filter(user_id_id=user_id).first()
    user_skills = User_skills.objects.filter(user_id_id=user_id).first()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        linkedin = request.POST.get('linkedin')
        summary = request.POST.get('summary')
        skills=request.POST.get('skills')
        if user_obj:
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = email
            user_obj.contact_no = contact_no
            user_obj.linkedin_url = linkedin
            user_obj.summary = summary
            user_obj.save()
            if user_skills:
                user_skills.skills = skills
                user_skills.save()
                return redirect('/add_experience_choice')
        else:
            user = Header.objects.create(first_name=first_name,last_name=last_name,email=email,
                              contact_no=contact_no,linkedin_url=linkedin,summary=summary,user_id_id=user_id)
            if not user_skills:
                data=User_skills.objects.create(skills=skills,user_id_id=user_id)
            if user:
                return redirect('/add_experience_choice')
    context = {
        't_image':t_image,
        'user_obj':user_obj,
        'user_skills':user_skills
    }
    return render(request,'personal_info.html',context)


@login_required(login_url='/login')
def extracted_personal_info(request, id):
    temp_image = TemplatesInfo.objects.get(id=id)
    print(temp_image.template_image)
    t_image = temp_image.template_image
    user_id=request.user.id
    details=NewUser.objects.filter(id=user_id).first()
    ex_details=Extracted_ResumeDetails.objects.filter(user_id_id=user_id).order_by('-id').first()
    user_obj = Header.objects.filter(user_id_id=user_id).first()
    user_skills = User_skills.objects.filter(user_id_id=user_id).first()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        linkedin = request.POST.get('linkedin')
        summary = request.POST.get('summary')
        skills=request.POST.get('skills')
        if user_obj:
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = email
            user_obj.contact_no = contact_no
            user_obj.linkedin_url = linkedin
            user_obj.summary = summary
            user_obj.save()
            if user_skills:
                user_skills.skills = skills
                user_skills.save()
                return redirect('/extracted_experience_choice')
        else:
            user = Header.objects.create(first_name=first_name,last_name=last_name,email=email,
                              contact_no=contact_no,linkedin_url=linkedin,summary=summary,user_id_id=user_id)
            if not user_skills:
                data=User_skills.objects.create(skills=skills,user_id_id=user_id)
            if user:
                return redirect('/extracted_experience_choice')
    
    context = {
        't_image':t_image,'details':details,'ex_details':ex_details
    }
    return render(request,'extracted_personal_info.html',context)

@login_required(login_url='/login')
def edit_personal_info(request,id):
    user_id=request.user.id
    details=Header.objects.get(user_id_id=user_id)
    skills=User_skills.objects.get(user_id_id=user_id)
    if request.method == 'POST':
        details.first_name = request.POST.get('first_name')
        details.last_name = request.POST.get('last_name')
        details.email = request.POST.get('email')
        details.contact_no = request.POST.get('contact_no')
        details.linkedin = request.POST.get('linkedin')
        details.summary = request.POST.get('summary')
        skills.skills=request.POST.get('skills')
        details.save()
        skills.save()
        return redirect('/template1/{}'.format(id))
    context = {
        'details':details,'skills':skills
    }
    return render(request,'edit_personal_info.html',context)

@login_required(login_url='/login')
def work_history(request):
    id = request.user.id
    print("hhhhhhhhhhhhhhhhhhhh")
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
            print("jjjjjjjjjjjjjj")
            return redirect('/add_experience_choice')
    return render(request, 'work_history.html')


@login_required(login_url='/login')
def edit_add_work_history(request,id):
    user_id = request.user.id
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
                                         to_date=to_date, description=description, user_id_id=user_id)
        if data:
            return redirect('/edit_experience_choice/{}'.format(id))
    return render(request, 'edit_add_work_history.html')

@login_required(login_url='/login')
def edit_work_history(request,id,template_id):
    print("hhhhhhhhhhhhhh",template_id)
    user_id = request.user.id
    details=Experience.objects.get(id=id)
    if request.method == 'POST':
        details.designation = request.POST.get('designation')
        details.company_name = request.POST.get('company_name')
        details.from_date = request.POST.get('from_date')
        details.to_date = request.POST.get('to_date')
        details.description = request.POST.get('description')
        
        if 'to_present' in request.POST:
            # If "To Present" checkbox is checked, set to_date to the current date
            details.to_date ='Present'  # Format to match your field type
        details.save()
        return redirect('/edit_experience_choice/{}'.format(template_id))
    context={'details':details}
    return render(request, 'edit_work_history.html',context)

@login_required(login_url='/login')
def education(request):
    user_id = request.user.id
    if request.method == 'POST':
        college_name = request.POST.get('college_name')
        degree = request.POST.get('degree')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        city = request.POST.get('city')
        cgpa = request.POST.get('cgpa')
        data=Education.objects.create(college_name=college_name,degree=degree,from_date=from_date,
                                      to_date=to_date,city=city,cgpa=cgpa,user_id_id=user_id)
        if data:
            return redirect('/add_education_choice')
    return render(request,'education.html')

@login_required(login_url='/login')
def edit_education(request,id):
    user_id = request.user.id
    if request.method == 'POST':
        college_name = request.POST.get('college_name')
        degree = request.POST.get('degree')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        city = request.POST.get('city')
        cgpa = request.POST.get('cgpa')
        data=Education.objects.create(college_name=college_name,degree=degree,from_date=from_date,
                                      to_date=to_date,city=city,cgpa=cgpa,user_id_id=user_id)
        if data:
            return redirect('/edit_education_choice/{}'.format(id))
    return render(request,'edit_education.html')

@login_required(login_url='/login')
def edit_education_form(request,id,template_id):
    user_id = request.user.id
    details=Education.objects.get(id=id)
    if request.method == 'POST':
        details.college_name = request.POST.get('college_name')
        details.degree = request.POST.get('degree')
        details.from_date = request.POST.get('from_date')
        details.to_date = request.POST.get('to_date')
        details.city = request.POST.get('city')
        details.cgpa = request.POST.get('cgpa')
        details.save()
        return redirect('/edit_education_choice/{}'.format(template_id))
    context={'details':details}
    return render(request,'edit_education_form.html',context)

@login_required(login_url='/login')
def extra_details(request):
    template_id = request.session.get('template_id')
    context = {
        'template_id':template_id
    }
    return render(request,'extra_details.html',context)

@login_required(login_url='/login')
def project_details(request):
    id = request.user.id
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        tools = request.POST.get('tools')
        link = request.POST.get('link')
        description = request.POST.get('description')
        data = Project.objects.create(project_name=project_name, project_link=link, tools_used=tools,
                                      description=description, user_id_id=id)
        return redirect('/extra_details')

@login_required(login_url='/login')
def certificates(request):
    id = request.user.id
    if request.method == 'POST':
        certificates = request.POST.get('certificates')
        data = Certificates.objects.create(certificates=certificates,user_id_id=id)
        return redirect('/extra_details')

@login_required(login_url='/login')
def languages(request):
    id = request.user.id
    if request.method == 'POST':
        languages_known = request.POST.get('languages_known')
        data = Languages.objects.create(languages_known=languages_known,user_id_id=id)
        return redirect('/extra_details')

@login_required(login_url='/login')
def edit_project(request,id):
    user_id=request.user.id
    details=Project.objects.filter(user_id_id=user_id)
    context={'details':details,'template_id':id}
    return render(request,'edit_project.html',context)

@login_required(login_url='/login')
def edit_project_form(request,id,template_id):
    user_id = request.user.id
    details=Project.objects.get(id=id)
    if request.method == 'POST':
        details.project_name = request.POST.get('project_name')
        details.tools = request.POST.get('tools')
        details.link = request.POST.get('link')
        details.description = request.POST.get('description')
        details.save()
        return redirect('/edit_project/{}'.format(template_id))
    context={'details':details}
    return render(request,'edit_project_form.html',context)

@login_required(login_url='/login')
def edit_project_details(request,id):
    user_id = request.user.id
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        tools = request.POST.get('tools')
        link = request.POST.get('link')
        description = request.POST.get('description')
        data = Project.objects.create(project_name=project_name, project_link=link, tools_used=tools,
                                      description=description, user_id_id=user_id)
        return redirect('/edit_project/{}'.format(id))


@login_required(login_url='/login')
def extracted_work_history(request):
    user_id = request.user.id
    details=Extracted_ExperienceDetails.objects.filter(user_id_id=user_id).order_by('-id').first()
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
                                         to_date=to_date, description=description, user_id_id=user_id)
        if data:
            return redirect('/extracted_experience_choice')
    context={'details':details}
    return render(request, 'extracted_work_history.html',context)

@login_required(login_url='/login')
def extracted_experience_choice(request):
    user_id=request.user.id
    details=Experience.objects.filter(user_id_id=user_id)
    context={'id':id,'details':details}
    return render(request,'extracted_experience_choice.html',context)

@login_required(login_url='/login')
def extracted_education(request):
    user_id = request.user.id
    details=Extracted_EducationDetails.objects.filter(user_id_id=user_id).order_by('-id').first()
    if request.method == 'POST':
        college_name = request.POST.get('college_name')
        degree = request.POST.get('degree')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        city = request.POST.get('city')
        cgpa = request.POST.get('cgpa')
        data=Education.objects.create(college_name=college_name,degree=degree,from_date=from_date,
                                      to_date=to_date,city=city,cgpa=cgpa,user_id_id=user_id)
        if data:
            return redirect('/extracted_education_choice')
    context={'id':id,'details':details}
    return render(request,'extracted_education.html',context)

@login_required(login_url='/login')
def extracted_education_choice(request):
    user_id=request.user.id
    details=Education.objects.filter(user_id_id=user_id)
    context={'id':id,'details':details}
    return render(request,'extracted_education_choice.html',context)

@login_required(login_url='/login')
def extracted_extra_details(request):
    template_id = request.session.get('template_id')
    print("iiiiiiii",template_id)
    context={'template_id':template_id}
    return render(request,'extracted_extra_details.html',context)


@login_required(login_url='/login')
def resume_options(request, id):
    i = request.user.id
    print(id)
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        Resume.objects.create(resume_file=resume,user_id_id=i,template_id=id)
        resume_path = Resume.objects.last().resume_file.path
        resume_details = extract_and_store_resume_data(resume_path, id, request.user.id)
        # Assuming 'personal_info' is the URL name for the next page
        return redirect('/extracted_personal_info/{}'.format(id))
    return render(request, 'resume_options.html', {'id': id})

@login_required(login_url='/login')
def extract_and_store_resume_data(resume_path,id, user_id):
    # Extract data from the resume
    images = convert_from_path(resume_path)
    extracted_text = ""
    for img in images:
        extracted_text += pytesseract.image_to_string(img)

    # Perform sentiment analysis on the extracted text using VADER
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(extracted_text)

    # Split the extracted text into separate lines
    split_text = extracted_text.split('\n')

    # Organize the data into separate categories
    data = {
        'sentiment': sentiment,
        'certifications': [],
        'skills': [],
        'experience': [],
        'education': [],
        'contact': [],
        'summary': [],
        'about': [],
        'achievements': [],
        'languages': [],
        'projects': [],
        'internship': [],
        'language': [],
        'declaration':[],
    }
    current_category = None
    for line in split_text:
        line = line.strip()
        if line.upper() in ['CERTIFICATIONS', 'SKILLS', 'EDUCATION', 'CONTACT', 'SUMMARY', 'ABOUT', 'ACHIEVEMENTS',
                            'LANGUAGES', 'PROJECTS', 'INTERNSHIP', 'LANGUAGE','DECLARATION']:
            current_category = line.upper()
        elif line.upper().startswith('EXPERIENCE') or line.upper().startswith('PROFESSIONAL EXPERIENCE'):
            current_category = 'EXPERIENCE'
        elif line.upper().startswith('SUMMARY') or line.upper().startswith('PROFILE SUMMARY'):
            current_category = 'SUMMARY'
        elif line.upper().startswith('ABOUT ME') or line.upper().startswith('PROFILE'):
            current_category = 'SUMMARY'
        elif line.upper().startswith('LANGUAGES') or line.upper().startswith('LANGUAGES KNOWN'):
            current_category = 'LANGUAGES'
        elif line.upper().startswith('SKILLS') or line.upper().startswith('KEY SKILLS'):
            current_category = 'SKILLS'
        elif line.upper().startswith('TECHNICAL SKILLS') or line.upper().startswith('EXPERTISE'):
            current_category = 'SKILLS'
        elif current_category:
            line = re.sub(r'[^\w\s]', '', line)
            data[current_category.lower()].append(line)
    # Join skills and summary lists into single strings
    data['summary'] = '\n'.join(data['summary'])
    first_project_line = ''
    for project_line in data['projects']:
        project_line = project_line.strip()
        if project_line:
            first_project_line = project_line
            break
    print("hhhh", first_project_line)
    data['education'] = '\n'.join(data['education'])
    data['internship'] = '\n'.join(data['internship'])
    data['experience'] = '\n'.join(data['experience'])
    data['contact'] = '\n'.join(data['contact'])
    data['certifications'] = '\n'.join(data['certifications'])
    # Filter out unwanted characters and join skills into a single string
    data['skills'] = ', '.join([skill.strip()[2:] for skill in data['skills'] if skill.strip().startswith('e ')])
    print("skills", data['skills'])
    data['languages'] = ', '.join([language.strip()[3:] for language in data['languages'] if language.strip().startswith('vy')])
    # Store the extracted data in the database
    resume_details = Extracted_ResumeDetails.objects.create(
        user_id_id=user_id,
        template_id=id,
        summary=data['summary'],
        skills=data['skills'],
        projects=first_project_line,
        languages=data['languages'],
        education=data['education'],
        internship=data['internship'],
        experience=data['experience'],
        contact=data['contact'],
        certifications=data['certifications'] 
    )
    education_lines = data['education'].split('\n')
    experience_lines = data['experience'].split('\n')

    # Extract degree details
    degree, university, year_of_passing = extract_degree_details(education_lines)

    # Extract experience details
    designation, company_name, start_date, end_date = extract_experience_details(experience_lines)

    # Store education details in the database
    Extracted_EducationDetails.objects.create(
        user_id_id=user_id,
        template_id=id,
        degree=degree,
        university=university,
        year_of_passing=year_of_passing
    )
    Extracted_ExperienceDetails.objects.create(
        user_id_id=user_id,
        template_id=id,
        company_name=company_name,
        start_date=start_date,
        end_date=end_date
    )
    return Extracted_ResumeDetails.objects.last()


@login_required(login_url='/login')
def extract_degree_details(education_lines):
    degree = ""
    university = ""
    year_of_passing = ""
    degree_keywords = ["degree", "bachelor", "master", "diploma", "puc", "business", "Btech"]
    year_regex = r'\b\d{4}\b'
    for line in education_lines:
        match = re.search(year_regex, line)
        if match:
            year_of_passing = match.group()
            month_match = re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', line, re.IGNORECASE)
            if month_match:
                year_of_passing += " " + month_match.group()
        elif any(keyword in line.lower() for keyword in degree_keywords):
            degree = line
        elif "college" in line.lower() or "university" in line.lower():
            university = line
    return degree, university, year_of_passing

@login_required(login_url='/login')
def extract_experience_details(experience_lines):
    designation = ""
    company_name = ""
    start_date = ""
    end_date = ""
    designation_keywords = ["Executive Secretary", "Secretary", "Assistant", "software", "engineer", "analyst",
                            "agent", 'manager']
    company_keywords = ["pvt ltd", "Company", "limited", "corp"]
    date_regex = r'\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\w+\s\d{4})\b'  # Matches YYYY-MM-DD, YYYY/MM/DD, MMM YYYY
    for line in experience_lines:
        if any(keyword in line for keyword in designation_keywords):
            designation = line.strip()
        if any(keyword in line for keyword in company_keywords):
            company_name = line.strip()
        match = re.search(date_regex, line)
        if match:
            if not start_date:
                start_date = match.group()
            else:
                end_date = match.group()
    return designation, company_name, start_date, end_date

@login_required(login_url='/login')
def template1(request,id):
    user_id = request.user.id
    template_id = id
    data = TemplatesInfo.objects.get(id=template_id)
    template_html_id = data.id_name
    personal_info = Header.objects.get(user_id_id=user_id)
    # fetching exp section
    exp_info = Experience.objects.filter(user_id_id=user_id)
    # education section
    edu_info = Education.objects.filter(user_id_id=user_id)
    pro_info = Project.objects.filter(user_id_id=user_id)
    # skills section
    skills_info = User_skills.objects.filter(user_id_id=user_id).first()
    s = skills_info.skills
    skills_list = [skill.strip() for skill in s.split(',')]
    print(skills_list)
    # certificates section
    certificates_info = Certificates.objects.filter(user_id_id=user_id).first()
    print(certificates_info)
    # Langages known
    lang_list = []
    lang_info = Languages.objects.filter(user_id_id=user_id).first()
    if lang_info:
        languages_known = lang_info.languages_known
        lang_list = [x.strip() for x in languages_known.split(',')]

    # templates 

    temp_data = TemplatesInfo.objects.all()

    
    context = {
        'template_html_id':template_html_id,
        'personal_info':personal_info,
        'exp_info':exp_info,
        'edu_info':edu_info,
        'pro_info':pro_info,
        'skills_list':skills_list,
        'certificates_info':certificates_info,
        'lang_list':lang_list,
        'temp_data':temp_data,
        'template_id':template_id
        
    }
    return render(request,'template1.html',context)

def set(request):
    return render(request,'set.html')
