from datetime import date

from django.test import TestCase
from django.urls import reverse

from edu.models import Editora, Livro


class ViewsTestCase(TestCase):
    def setUp(self):
        self.editora = Editora.objects.create(nome='Editora V')
        for i in range(15):
            Livro.objects.create(
                isbn=f'978000000000{i}',
                titulo=f'Livro {i}',
                publicacao=date(2022, 1, 1),
                preco='20.00',
                estoque=3,
                editora=self.editora,
            )

    def test_listar_livros_pagina_principal(self):
        url = reverse('listar_livros')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Deve conter o contexto 'livros' e paginar (10 por página)
        self.assertIn('livros', response.context)
        self.assertEqual(len(response.context['livros']), 10)
