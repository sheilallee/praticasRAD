from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Livro
from .forms import LivroForm
from .constants import ANALISTAS_GROUP_NAME
from django.utils.translation import gettext as _


def _usuario_no_grupo_analistas(user):
    return user.is_authenticated and user.groups.filter(name=ANALISTAS_GROUP_NAME).exists()


def _usuario_pode_gerenciar_livro(user, permissao):
    # Regra estrita: precisa pertencer ao grupo de analistas e ter a permissao especifica.
    return _usuario_no_grupo_analistas(user) and user.has_perm(permissao)


def listar_livros(request):
    """
    View que lista os livros com paginação (10 livros por página).
    """
    livros_lista = Livro.objects.all().order_by('titulo')
    paginator = Paginator(livros_lista, 10)
    numero_pagina = request.GET.get('page', 1)
    livros = paginator.get_page(numero_pagina)

    contexto = {
        'livros': livros,
        'paginator': paginator,
        'numero_pagina': numero_pagina,
        'can_add_livro': _usuario_pode_gerenciar_livro(request.user, 'edu.add_livro'),
        'can_change_livro': _usuario_pode_gerenciar_livro(request.user, 'edu.change_livro'),
        'can_delete_livro': _usuario_pode_gerenciar_livro(request.user, 'edu.delete_livro'),
    }
    return render(request, 'edu/listar_livros.html', contexto)

@login_required(login_url='login')
def livro_criar(request):
    if not _usuario_pode_gerenciar_livro(request.user, 'edu.add_livro'):
        messages.error(request, _('Você não tem permissão para cadastrar livros.'))
        return redirect('listar_livros')

    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Livro criado com sucesso!'))
            return redirect('listar_livros')
    else:
        form = LivroForm()

    return render(request, 'edu/livro_form.html', {'form': form, 'titulo_pagina': _('Cadastrar Livro')})

@login_required(login_url='login')
def livro_editar(request, pk):
    if not _usuario_pode_gerenciar_livro(request.user, 'edu.change_livro'):
        messages.error(request, _('Você não tem permissão para editar livros.'))
        return redirect('listar_livros')

    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, _('Livro atualizado com sucesso!'))
            return redirect('listar_livros')
    else:
        form = LivroForm(instance=livro)

    return render(request, 'edu/livro_form.html', {'form': form, 'titulo_pagina': _('Editar Livro')})

@login_required(login_url='login')
def livro_remover(request, pk):
    if not _usuario_pode_gerenciar_livro(request.user, 'edu.delete_livro'):
        messages.error(request, _('Você não tem permissão para remover livros.'))
        return redirect('listar_livros')

    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, _('Livro removido com sucesso!'))
        return redirect('listar_livros')

    return render(request, 'edu/livro_confirm_delete.html', {'livro': livro})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Cadastro realizado com sucesso!'))
            return redirect('listar_livros')
    else:
        form = UserCreationForm()
    return render(request, 'edu/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('Login realizado com sucesso!'))
            return redirect(request.GET.get('next', 'listar_livros'))
    else:
        form = AuthenticationForm()
    return render(request, 'edu/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, _('Logout realizado com sucesso!'))
    return redirect('home')
