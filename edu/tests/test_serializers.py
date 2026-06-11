from django.test import TestCase

from edu.serializers import AutorSerializer, EditoraSerializer


class SerializersTestCase(TestCase):
    def test_autor_serializer_valid(self):
        data = {'nome': 'Autor S'}
        serializer = AutorSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_editora_serializer_invalid_nome_vazio(self):
        data = {'nome': ''}
        serializer = EditoraSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)
