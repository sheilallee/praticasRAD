from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Lista todos os usuários do sistema'

    def handle(self, *args, **options):
        users = User.objects.all()
        if users:
            self.stdout.write('Usuários existentes:')
            for user in users:
                status = 'Ativo' if user.is_active else 'Inativo'
                self.stdout.write(f'- {user.username}: {status}')
        else:
            self.stdout.write('Nenhum usuário encontrado no banco de dados.')