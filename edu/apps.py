from django.apps import AppConfig


class EduConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edu'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Livro

        try:
            livro_ct = ContentType.objects.get_for_model(Livro)
            permission_codenames = ['add_livro', 'change_livro', 'delete_livro']
            permissions = Permission.objects.filter(content_type=livro_ct, codename__in=permission_codenames)
            group, created = Group.objects.get_or_create(name='Analistas de Cadastro de Produtos')
            group.permissions.set(permissions)
        except Exception:
            # O banco de dados pode não estar pronto no momento da inicialização.
            pass
