#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.contrib.auth.models import User

print('Verificando usuários existentes...')
users = User.objects.all()
if users:
    print('Usuários encontrados:')
    for user in users:
        status = 'Ativo' if user.is_active else 'Inativo'
        print(f'- {user.username}: {status}')
else:
    print('Nenhum usuário encontrado. Criando usuário admin...')

    # Criar usuário admin
    try:
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='123',
            is_staff=True,
            is_superuser=True
        )
        user.save()
        print('✅ Usuário admin criado com sucesso!')
        print('   Usuário: admin')
        print('   Senha: 123')
    except Exception as e:
        print(f'❌ Erro ao criar usuário: {e}')