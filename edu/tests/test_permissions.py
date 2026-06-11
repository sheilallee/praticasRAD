from datetime import date

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from edu.constants import ANALISTAS_GROUP_NAME
from edu.models import Editora, Livro


class LivroAutorizacaoTests(TestCase):
    def setUp(self):
        self.editora = Editora.objects.create(nome='Editora Teste')
        self.livro = Livro.objects.create(
            isbn='1234567890123',
            titulo='Livro Base',
            publicacao=date(2024, 1, 1),
            preco='99.90',
            estoque=10,
            editora=self.editora,
        )

        livro_ct = ContentType.objects.get_for_model(Livro)
        codenames = ['add_livro', 'change_livro', 'delete_livro']
        permissions = Permission.objects.filter(content_type=livro_ct, codename__in=codenames)

        self.grupo_analistas, _ = Group.objects.get_or_create(name=ANALISTAS_GROUP_NAME)
        self.grupo_analistas.permissions.set(permissions)

        self.usuario_analista = User.objects.create_user(username='analista', password='123456')
        self.usuario_analista.groups.add(self.grupo_analistas)

        self.usuario_comum = User.objects.create_user(username='comum', password='123456')

        self.usuario_com_perm_direta = User.objects.create_user(username='perm_direta', password='123456')
        self.usuario_com_perm_direta.user_permissions.set(permissions)

    def test_usuario_nao_autenticado_redireciona_para_login(self):
        response = self.client.get(reverse('livro_criar'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_usuario_comum_nao_gerencia_livros(self):
        self.client.login(username='comum', password='123456')
        response = self.client.get(reverse('livro_criar'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Você não tem permissão para cadastrar livros.')
        self.assertEqual(Livro.objects.count(), 1)

    def test_usuario_com_permissao_direta_sem_grupo_nao_gerencia_livros(self):
        self.client.login(username='perm_direta', password='123456')
        response = self.client.get(reverse('livro_criar'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Você não tem permissão para cadastrar livros.')

    def test_usuario_analista_consegue_criar_editar_e_remover_livro(self):
        self.client.login(username='analista', password='123456')

        response_create = self.client.post(
            reverse('livro_criar'),
            {
                'isbn': '9876543210123',
                'titulo': 'Livro Novo',
                'publicacao': '2025-01-01',
                'preco': '55.50',
                'estoque': 15,
                'editora': self.editora.pk,
            },
        )
        self.assertEqual(response_create.status_code, 302)
        self.assertTrue(Livro.objects.filter(isbn='9876543210123').exists())

        response_edit = self.client.post(
            reverse('livro_editar', args=[self.livro.pk]),
            {
                'isbn': self.livro.isbn,
                'titulo': 'Livro Atualizado',
                'publicacao': self.livro.publicacao,
                'preco': self.livro.preco,
                'estoque': self.livro.estoque,
                'editora': self.editora.pk,
            },
        )
        self.assertEqual(response_edit.status_code, 302)
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.titulo, 'Livro Atualizado')

        response_delete = self.client.post(reverse('livro_remover', args=[self.livro.pk]))
        self.assertEqual(response_delete.status_code, 302)
        self.assertFalse(Livro.objects.filter(pk=self.livro.pk).exists())

    def test_template_nao_exibe_acoes_para_usuario_sem_grupo(self):
        self.client.login(username='perm_direta', password='123456')
        response = self.client.get(reverse('listar_livros'))

        self.assertNotContains(response, 'Novo Livro')
        self.assertNotContains(response, 'Editar')
        self.assertNotContains(response, 'Remover')

    def test_template_exibe_acoes_para_analista(self):
        self.client.login(username='analista', password='123456')
        response = self.client.get(reverse('listar_livros'))

        self.assertContains(response, 'Novo Livro')
        self.assertContains(response, 'Editar')
        self.assertContains(response, 'Remover')
