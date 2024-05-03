from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('login',views.login_view,name='login_view'),
    path('registration',views.registration,name='registration'),
    path('',views.index,name="index"),
    path('resumes',views.resumes,name="resumes"),
    path('resume_options',views.resume_options,name="resume_options"),
    
]