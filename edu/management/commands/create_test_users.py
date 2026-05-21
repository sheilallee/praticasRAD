from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from edu.constants import ANALISTAS_GROUP_NAME
from edu.models import Livro


class Command(BaseCommand):
    help = 'Cria usuarios de teste para validar autorizacao de gerenciamento de livros.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            default='123456',
            help='Senha padrao para os usuarios de teste (default: 123456).',
        )

    def handle(self, *args, **options):
        password = options['password']

        livro_ct = ContentType.objects.get_for_model(Livro)
        permission_codenames = ['add_livro', 'change_livro', 'delete_livro']
        permissions = Permission.objects.filter(content_type=livro_ct, codename__in=permission_codenames)

        grupo, _ = Group.objects.get_or_create(name=ANALISTAS_GROUP_NAME)
        grupo.permissions.set(permissions)

        analistas = ['analista_produto_1', 'analista_produto_2']
        nao_analistas = ['usuario_comum_1', 'usuario_comum_2']

        for username in analistas + nao_analistas:
            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.is_active = True
            user.save()

            user.groups.clear()
            user.user_permissions.clear()

            if username in analistas:
                user.groups.add(grupo)

            status = 'criado' if created else 'atualizado'
            tipo = 'analista' if username in analistas else 'nao analista'
            self.stdout.write(self.style.SUCCESS(f'Usuario {username} ({tipo}) {status}.'))

        self.stdout.write('Usuarios de teste prontos para validacao da Pratica 08.')