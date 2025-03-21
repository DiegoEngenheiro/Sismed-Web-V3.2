from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importe o sistema de mensagens do Django

# Função para cadastro de usuários
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se o usuário já existe
        user = User.objects.filter(username=username).first()

        if user:
            messages.error(request, 'Já existe um usuário com este nome de usuário.')
            return render(request, 'cadastro.html')  # Renderiza a mesma página com a mensagem de erro

        # Cria o usuário
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        messages.success(request, 'Usuário cadastrado com sucesso! Redirecionando para o login...')
        return render(request, 'cadastro.html')  # Renderiza a mesma página com a mensagem de sucesso

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
        messages.success(request, 'Login realizado com sucesso!')  # Mensagem de sucesso
        return redirect('clientes')  # Redirecionar para a página de clientes
    else:
        messages.error(request, 'Email ou senha inválidos.')  # Exibe mensagem de erro
        return render(request, 'login.html')  # Renderiza a mesma página com a mensagem de erro

@login_required(login_url='/usuarios/login/')  # Requer login para acessar a plataforma
def logout(request):
    django_logout(request)  # Realiza o logout
    messages.success(request, 'Você foi desconectado com sucesso.')  # Exibe mensagem de sucesso
    return redirect('login')  # Redireciona para a página de login
