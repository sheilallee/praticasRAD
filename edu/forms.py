from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['isbn', 'titulo', 'publicacao', 'preco', 'estoque', 'editora']
        labels = {
            'isbn': _('ISBN'),
            'titulo': _('Título'),
            'publicacao': _('Publicação'),
            'preco': _('Preço'),
            'estoque': _('Estoque'),
            'editora': _('Editora'),
        }
        widgets = {
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'publicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'editora': forms.Select(attrs={'class': 'form-control'}),
        }
