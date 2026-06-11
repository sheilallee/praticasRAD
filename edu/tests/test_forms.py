from datetime import date

from django.test import TestCase

from edu.forms import LivroForm
from edu.models import Editora


class FormsTestCase(TestCase):
    def setUp(self):
        self.editora = Editora.objects.create(nome='Editora F')

    def test_livro_form_valido(self):
        form_data = {
            'isbn': '1112223334445',
            'titulo': 'Form Teste',
            'publicacao': date.today(),
            'preco': '12.00',
            'estoque': 2,
            'editora': self.editora.pk,
        }
        form = LivroForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_livro_form_invalido_sem_isbn(self):
        form_data = {
            'isbn': '',
            'titulo': 'Form Teste',
            'publicacao': date.today(),
            'preco': '12.00',
            'estoque': 2,
            'editora': self.editora.pk,
        }
        form = LivroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)
