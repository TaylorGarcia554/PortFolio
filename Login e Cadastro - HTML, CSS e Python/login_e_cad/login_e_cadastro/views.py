from django.shortcuts import render
from .models import usuarios

# Create your views here.

def index(request):
    return render(request, "usuarios/login.html")

def cadastro(request):
    # Salvar os dados da tela para o banco de dados.
    novo_usuario = usuarios()
    novo_usuario.nome = request.POST.get('nome')
    novo_usuario.email = request.POST.get('email')
    novo_usuario.telefone = request.POST.get('telefone')
    novo_usuario.senha = request.POST.get('senha')
    return render(request, "usuarios/cadastro.html")
    
