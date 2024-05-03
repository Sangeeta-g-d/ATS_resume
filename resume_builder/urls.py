from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('login',views.login_view,name='login_view'),
    path('registration',views.registration,name='registration'),
    path('',views.index,name="index"),
    path('resumes',views.resumes,name="resumes"),
    path('resume_options',views.resume_options,name="resume_options"),
    path('personal_info',views.personal_info,name="personal_info"),
    path('work_history',views.work_history,name="work_history"),
    path('education',views.education,name="education"),
    path('extra_details',views.extra_details,name="extra_details"),
    path('add_experience_choice',views.add_experience_choice,name="add_experience_choice"),
    path('add_education_choice',views.add_education_choice,name="add_education_choice"),
    
]