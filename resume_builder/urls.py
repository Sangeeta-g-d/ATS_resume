from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('login',views.login_view,name='login_view'),
    path('registration',views.registration,name='registration'),
    path('',views.index,name="index"),
    path('resumes',views.resumes,name="resumes"),
    path('resume_options/<int:id>',views.resume_options,name="resume_options"),
    path('personal_info/<int:id>',views.personal_info,name="personal_info"),
    path('extracted_personal_info/<int:id>',views.extracted_personal_info,name="extracted_personal_info"),
    path('work_history',views.work_history,name="work_history"),
    path('extracted_work_history',views.extracted_work_history,name="extracted_work_history"),
    path('education',views.education,name="education"),
    path('extra_details',views.extra_details,name="extra_details"),
    path('add_experience_choice',views.add_experience_choice,name="add_experience_choice"),
    path('extracted_experience_choice',views.extracted_experience_choice,name="extracted_experience_choice"),
path('extracted_education_choice',views.extracted_education_choice,name="extracted_education_choice"),
    path('extracted_education',views.extracted_education,name="extracted_education"),
    path('extracted_extra_details',views.extracted_extra_details,name="extracted_extra_details"),
    path('add_education_choice',views.add_education_choice,name="add_education_choice"),
    path('project_details',views.project_details,name="project_details"),
    path('certificates',views.certificates,name="certificates"),
    path('languages',views.languages,name="languages"),
    path('add_template',views.add_template,name="add_template"),
    path('template1',views.template1,name="template1"),
    path('set',views.set,name="set"),
    path('edit_personal_info',views.edit_personal_info,name="edit_personal_info"),
    
]