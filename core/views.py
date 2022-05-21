from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.models import Evento


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)  # noqa pega os dados do banco de dados
    dados = {'eventos': evento}
    return render(request, 'core/agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    return render(request, 'core/evento.html')


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        Evento.objects.create(
            titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario, local=local)  # noqa
    return redirect('/')


def login_user(request):
    return render(request, 'core/login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username-login')
        password = request.POST.get('password-login')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return redirect('/')
