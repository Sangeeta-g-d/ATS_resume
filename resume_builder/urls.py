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
     path('delete_experience/<int:experience_id>/', views.delete_experience, name='delete_experience'),
    path('delete_education/<int:education_id>/', views.delete_education, name='delete_education'),

    path('extracted_work_history',views.extracted_work_history,name="extracted_work_history"),
    path('education',views.education,name="education"),
    path('extra_details',views.extra_details,name="extra_details"),
    path('add_experience_choice',views.add_experience_choice,name="add_experience_choice"),
    path('edit_experience_choice/<int:id>',views.edit_experience_choice,name="edit_experience_choice"),
    path('extracted_experience_choice',views.extracted_experience_choice,name="extracted_experience_choice"),
    path('extracted_education_choice',views.extracted_education_choice,name="extracted_education_choice"),
    path('extracted_education',views.extracted_education,name="extracted_education"),
    path('extracted_extra_details',views.extracted_extra_details,name="extracted_extra_details"),
    path('add_education_choice',views.add_education_choice,name="add_education_choice"),
    path('edit_education_choice/<int:id>',views.edit_education_choice,name="edit_education_choice"),
    path('project_details',views.project_details,name="project_details"),
    path('certificates',views.certificates,name="certificates"),
    path('languages',views.languages,name="languages"),
    path('add_template',views.add_template,name="add_template"),
    path('template1/<int:id>',views.template1,name="template1"),
    path('set',views.set,name="set"),
    path('edit_personal_info/<int:id>',views.edit_personal_info,name="edit_personal_info"),
    path('edit_work_history/<int:id>/<int:template_id>',views.edit_work_history,name="edit_work_history"),
    path('edit_add_work_history/<int:id>',views.edit_add_work_history,name="edit_add_work_history"),
    path('edit_education_form/<int:id>/<int:template_id>',views.edit_education_form,name="edit_education_form"),
    path('edit_education/<int:id>',views.edit_education,name="edit_education"),
    path('edit_project/<int:id>',views.edit_project,name="edit_project"),
    path('edit_project_details/<int:id>',views.edit_project_details,name="edit_project_details"),
    path('edit_project_form/<int:id>/<int:template_id>',views.edit_project_form,name="edit_project_form"),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    
]