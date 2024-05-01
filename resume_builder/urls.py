from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
        path('',views.login_view,name='login_view'),
        path('registration',views.registration,name='registration'),
]