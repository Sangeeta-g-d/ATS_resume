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
from datetime import datetime
# Create your views here.

def add_template(request):
    if request.method == 'POST':
        view_name = request.POST.get('view_name')
        image = request.FILES.get('image')

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
            return redirect('resumes')
            return redirect('/resumes')
        else:
           
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'login.html')
    

def index(request):
    return render(request,'index.html')


def resumes(request):
    id=request.user.id
    print(id)
    templates = TemplatesInfo.objects.all()
    context = {
        'templates':templates
    }
    return render(request,'resumes.html', context)

def add_experience_choice(request):
    user_id=request.user.id
    details=Experience.objects.filter(user_id_id=user_id)
    context={'details':details}
    return render(request,'add_experience_choice.html',context)

def add_education_choice(request):
    user_id=request.user.id
    details=Education.objects.filter(user_id_id=user_id)
    context={'details':details}
    return render(request,'add_education_choice.html',context)


def personal_info(request, id):
    request.session['template_id'] = id
    temp_image = TemplatesInfo.objects.get(id=id)
    print(temp_image.template_image)
    t_image = temp_image.template_image
    user_id=request.user.id
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
        data=User_skills.objects.create(skills=skills,user_id_id=user_id)
        if user:
            return redirect('work_history')
    context = {
        't_image':t_image
    }
    return render(request,'personal_info.html',context)



def edit_personal_info(request):
    user_id=request.user.id
    print(user_id)
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
        return redirect('template1')
    context = {
        'details':details,'skills':skills
    }
    return render(request,'edit_personal_info.html',context)


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
            return redirect('add_education_choice')
    return render(request,'education.html')

def extra_details(request):
    return render(request,'extra_details.html')


def project_details(request):
    id = request.user.id
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        tools = request.POST.get('tools')
        link = request.POST.get('link')
        description = request.POST.get('description')
        data = Project.objects.create(project_name=project_name, project_link=link, tools_used=tools,
                                      description=description, user_id_id=id)
        return redirect('extra_details')


def certificates(request):
    id = request.user.id
    if request.method == 'POST':
        certificates = request.POST.get('certificates')
        data = Certificates.objects.create(certificates=certificates,user_id_id=id)
        return redirect('extra_details')


def languages(request):
    id = request.user.id
    if request.method == 'POST':
        languages_known = request.POST.get('languages_known')
        data = Languages.objects.create(languages_known=languages_known,user_id_id=id)
        return redirect('extra_details')



def extracted_personal_info(request, id):
    temp_image = TemplatesInfo.objects.get(id=id)
    print(temp_image.template_image)
    t_image = temp_image.template_image
    user_id=request.user.id
    details=NewUser.objects.filter(id=user_id).first()
    ex_details=Extracted_ResumeDetails.objects.filter(user_id_id=user_id).order_by('-id').first()
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
        data=User_skills.objects.create(skills=skills,user_id_id=user_id)
        if user:
            return redirect('extracted_work_history')
    context = {
        't_image':t_image,'details':details,'ex_details':ex_details
    }
    return render(request,'extracted_personal_info.html',context)


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
            return redirect('extracted_experience_choice')
    context={'details':details}
    return render(request, 'extracted_work_history.html',context)


def extracted_experience_choice(request):
    user_id=request.user.id
    details=Experience.objects.filter(user_id_id=user_id)
    context={'id':id,'details':details}
    return render(request,'extracted_experience_choice.html',context)


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
            return redirect('extracted_education_choice')
    context={'id':id,'details':details}
    return render(request,'extracted_education.html',context)


def extracted_education_choice(request):
    user_id=request.user.id
    details=Education.objects.filter(user_id_id=user_id)
    context={'id':id,'details':details}
    return render(request,'extracted_education_choice.html',context)



def extracted_extra_details(request):
    context={'id':id}
    return render(request,'extracted_extra_details.html')



def resume_options(request, id):
    i = request.user.id
    print(id)
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        Resume.objects.create(resume_file=resume,user_id_id=i,template_id=id)
        resume_path = Resume.objects.last().resume_file.path
        resume_details = extract_and_store_resume_data(resume_path, id, request.user.id)
        # Assuming 'personal_info' is the URL name for the next page
        return redirect('extracted_personal_info', id=id)
    return render(request, 'resume_options.html', {'id': id})

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

def template1(request):
    user_id=request.user.id
    print(user_id)
    template_id = request.session.get('template_id')
    data = TemplatesInfo.objects.get(id=template_id)
    template_html_id = data.id_name
    exp=Experience.objects.filter(user_id_id=user_id)
    context = {
        'template_html_id':template_html_id,'exp':exp
    }
    return render(request,'template1.html',context)

def set(request):
    return render(request,'set.html')
