from django.contrib import admin
from .models import Autor, Editora, Livro, Publica


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    search_fields = ('nome',)


@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    search_fields = ('nome',)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'titulo', 'editora', 'publicacao', 'preco', 'estoque')
    search_fields = ('titulo', 'isbn')


@admin.register(Publica)
class PublicaAdmin(admin.ModelAdmin):
    list_display = ('livro', 'autor')
    search_fields = ('livro__titulo', 'autor__nome')
