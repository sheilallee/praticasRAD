from datetime import date

from django.test import TestCase

from edu.models import Autor, Editora, Livro


class ModelsTestCase(TestCase):
    def test_str_representations_and_relations(self):
        editora = Editora.objects.create(nome='Editora X')
        autor = Autor.objects.create(nome='Autor Y')

        livro = Livro.objects.create(
            isbn='0001112223334',
            titulo='Título Teste',
            publicacao=date(2023, 1, 1),
            preco='10.50',
            estoque=5,
            editora=editora,
        )

        # __str__ checks
        self.assertEqual(str(editora), 'Editora X')
        self.assertEqual(str(autor), 'Autor Y')
        self.assertIn('Título Teste', str(livro))

        # relation Publica
        publica = livro.publicacoes.create(autor=autor)
        self.assertIn(str(autor), str(publica))
        self.assertIn(str(livro), str(publica))
