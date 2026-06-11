from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from edu.models import Autor, Editora


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.autor = Autor.objects.create(nome='Autor API')
        self.editora = Editora.objects.create(nome='Editora API')

    def test_list_autores(self):
        response = self.client.get('/api/autores/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_create_and_retrieve_editora(self):
        # create
        response_create = self.client.post('/api/editoras/', {'nome': 'Nova Editora'}, format='json')
        self.assertIn(response_create.status_code, (200, 201))
        # list
        response_list = self.client.get('/api/editoras/')
        self.assertEqual(response_list.status_code, 200)
        nomes = [e['nome'] for e in response_list.data]
        self.assertIn('Nova Editora', nomes)
