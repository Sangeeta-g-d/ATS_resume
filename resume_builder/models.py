from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class NewUser(AbstractUser):
    contact_no = models.CharField(max_length=100, default='9999999999')

class Header(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=800,default='first name')
    last_name = models.CharField(max_length=800,default='last name')
    contact_no = models.CharField(max_length=800,default='contact number')
    email = models.CharField(max_length=800,default='email')
    linkedin_url = models.CharField(max_length=800,default='linkedin url')
    summary = models.CharField(max_length=800,default='profile summary')


class Education(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    college_name = models.CharField(max_length=800,default='college name')
    degree = models.CharField(max_length=800,default='education')
    from_date = models.CharField(max_length=800,default='from date')
    to_date = models.CharField(max_length=800,default='to date')
    city = models.CharField(max_length=800,default='city')
    cgpa = models.CharField(max_length=800,default='CGPA')

class Experience(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    designation = models.CharField(max_length=800,default='designation')
    company_name = models.CharField(max_length=800,default='company name')
    from_date = models.CharField(max_length=800,default='from date')
    to_date = models.CharField(max_length=800,default='to date')
    description = models.CharField(max_length=1000,default='experience description')

class User_skills(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    skills = models.CharField(max_length=800,default='skills')

class Project(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=800,default='project_name')
    tools_used = models.CharField(max_length=800,default='company name')
    project_link = models.CharField(max_length=800,default='project link')
    description = models.CharField(max_length=1000,default='project description')

class Languages(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    languages_known = models.CharField(max_length=800,default='languages known')

class Achievements(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    acheivements = models.CharField(max_length=800,default='achievements')

class Certificates(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    certificates = models.CharField(max_length=800,default='certificates')

class TemplatesInfo(models.Model):
    template_image = models.ImageField(upload_to='uploaded_images/',default="profile")
    view_name = models.CharField(max_length=300,default='none')
    id_name=models.CharField(max_length=300,default='none')


class Resume(models.Model):
    resume_file = models.FileField(upload_to='resumes/')
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    template_id = models.CharField(max_length=50, default='0')

class Extracted_ResumeDetails(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    template_id = models.CharField(max_length=50, default='0')
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    summary=models.CharField(max_length=5000, default='Add Your Summry')
    skills=models.CharField(max_length=5000, default='Add Your Skills')
    projects=models.CharField(max_length=5000, default='Add Your projects')
    languages=models.CharField(max_length=5000, default='Add Your languages')
    education=models.CharField(max_length=5000, default='Add Your education')
    internship=models.CharField(max_length=5000, default='Add Your internship')
    experience=models.CharField(max_length=5000, default='Add Your experience')
    contact=models.CharField(max_length=5000, default='Add Your contact')
    certifications=models.CharField(max_length=5000, default='Add Your certifications')

class Extracted_ExperienceDetails(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    template_id = models.CharField(max_length=50, default='0')
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    company_name=models.CharField(max_length=5000, default='Add Your university')
    designation=models.CharField(max_length=5000, default='Add Your Designation')
    start_date=models.CharField(max_length=5000, default='Add Your Start date')
    end_date=models.CharField(max_length=5000, default='Add Your end date')


class Extracted_EducationDetails(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    template_id = models.CharField(max_length=50, default='0')
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    degree=models.CharField(max_length=5000, default='Add Your Degree')
    university=models.CharField(max_length=5000, default='Add Your university')
    year_of_passing=models.CharField(max_length=5000, default='Add Your year of passing')
    id_name = models.CharField(max_length=300,default='none')
