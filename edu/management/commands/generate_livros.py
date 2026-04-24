from django.core.management.base import BaseCommand
from faker import Faker
from edu.models import Livro, Editora
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Gera 100 registros de livros com dados realistas usando Faker'

    def handle(self, *args, **options):
        fake = Faker('pt_BR')  # Usar locale português Brasil
        
        # Criar algumas editoras se não existirem
        editoras = []
        nomes_editoras = [
            'Companhia das Letras',
            'Record',
            'Rocco',
            'Intrínseca',
            'Globo Livros'
        ]
        
        for nome in nomes_editoras:
            editora, criado = Editora.objects.get_or_create(nome=nome)
            editoras.append(editora)
        
        # Gerar 100 livros
        livros_criados = 0
        for i in range(100):
            try:
                # Usar ISBN como chave única a cada iteração
                isbn = fake.isbn13()
                titulo = fake.sentence(nb_words=6).capitalize()
                publicacao = fake.date_between(start_date='-30y')
                # Gerar preço aleatório entre 10 e 150
                preco = Decimal(random.randint(1000, 15000)) / 100
                estoque = random.randint(0, 100)
                editora = random.choice(editoras)
                
                # Criar o livro
                livro = Livro.objects.create(
                    isbn=isbn,
                    titulo=titulo,
                    publicacao=publicacao,
                    preco=preco,
                    estoque=estoque,
                    editora=editora,
                )
                
                livros_criados += 1
                    
            except Exception as e:
                # Continua si há erro (ex: ISBN duplicado)
                continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {livros_criados} livros foram criados com sucesso!'
            )
        )
