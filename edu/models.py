from django.db import models


class Autor(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Editora(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    titulo = models.CharField(max_length=200)
    publicacao = models.DateField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.IntegerField()
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE, related_name='livros')

    def __str__(self):
        return f"{self.titulo} ({self.isbn})"


class Publica(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='publicacoes')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='publicacoes')

    class Meta:
        unique_together = ('livro', 'autor')

    def __str__(self):
        return f"{self.livro} - {self.autor}"
