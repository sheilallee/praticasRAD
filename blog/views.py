from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime

# Create your views here.

def welcome(request):
    return HttpResponse('Bem-vindo ao meu blog!')

def eco(request, texto):
    return HttpResponse(f'Você digitou: {texto}')

def info(request):
    dados = {
        "disciplina": "RAD",
        "framework": "Django",
        "semestre": "2026.1"
    }
    return JsonResponse(dados)

# Prática Django DTL

def home(request):
    if request.user.is_authenticated:
        nome_usuario = request.user.username
        role = 'admin' if request.user.is_superuser else 'user'
        is_logged_in = True
    else:
        nome_usuario = 'Visitante'
        role = 'visitor'
        is_logged_in = False

    contexto = {
        'nome_usuario': nome_usuario,
        'now': datetime.now(),
        'is_logged_in': is_logged_in,
        'role': role,
        'produtos': [
            {'nome': 'TV LG 55"', 'preco': '2.500,00'},
            {'nome': 'Geladeira Frost Free', 'preco': '4.000,00'},
            {'nome': 'Fogão 5 Bocas', 'preco': '1.200,00'},
            {'nome': 'Micro-ondas 30L', 'preco': '800,00'},
            {'nome': 'Máquina de Lavar 12kg', 'preco': '2.200,00'},
            {'nome': 'Ar Condicionado 12000 BTUs', 'preco': '1.800,00'},
        ]
    }
    return render(request, 'blog/home.html', contexto)

def contato(request, telefone):

    telefone_formatado = telefone
    if len(telefone) == 11:
        
        telefone_formatado = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:
        
        telefone_formatado = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    
    contexto = {
        'telefone_formatado': telefone_formatado,
    }
    return render(request, 'blog/contato.html', contexto)
