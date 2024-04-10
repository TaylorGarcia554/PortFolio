
from django.contrib import admin
from django.urls import path
from login_e_cadastro import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro')
]
