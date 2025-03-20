from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

# Função para cadastro de usuários
def cadastro(request):
   if request.method == "GET":
      return render(request, 'cadastro.html')
   else:
      username = request.POST.get('username')
      email = request.POST.get('email')
      senha = request.POST.get('senha')

      user = User.objects.filter(username=username).first()

      if user:
         return HttpResponse('Já existe um usuário com este username')
      
      user = User.objects.create_user(username=username, email=email, password= senha)
      user.save()

      return HttpResponse('Usuário cadastrado com sucesso!')


# Função para login de usuários
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    # Para POST
    username = request.POST.get('username')  # Capturar o nome de usuário
    senha = request.POST.get('senha')  # Capturar a senha

    user = authenticate(username=username, password=senha)  # Autenticar o usuário

    if user is not None:
        login_django(request, user)  # Efetuar o login
        return redirect('clientes')  # Redirecionar para a página de clientes
    else:
        return HttpResponse('Email ou senha inválidos')  # Erro de autenticação
   

@login_required(login_url='/usuarios/login/')  # Requer login para acessar a plataforma
def logout(request):
    django_logout(request)  # Realiza o logout
    return redirect('login')  # Redireciona para a página de login