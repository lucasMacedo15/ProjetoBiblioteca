from django.db import models
from django.utils import timezone
from usuarios.models import Usuario
# Create your models here.


class Categoria(models.Model):

    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome


class Livros(models.Model):
    img = models.ImageField(upload_to='capa_livro', null=True, blank=True)
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=30)
    co_autor = models.CharField(max_length=30, blank=True, null=True)
    data_cadastro = models.DateField(default=timezone.now())
    emprestado = models.BooleanField(default=False)

    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)

    class Meta:
        verbose_name = 'Livro'

    def __str__(self) -> str:
        return self.nome


class Emprestimos(models.Model):
    choices = (
        ('P', 'Péssimo'), ('R', 'Ruim'), ('B', 'Bom'), ('O', 'Ótimo')
    )
    nome_emprestado = models.ForeignKey(
        Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
    nome_emprestado_anonimo = models.CharField(
        max_length=30, blank=True, null=True)
    data_emprestimo = models.DateTimeField(default=timezone.now())
    data_devolucao = models.DateTimeField(
        blank=True, null=True, default=timezone.now())
    livro = models.ForeignKey(Livros, models.DO_NOTHING)
    avaliacao = models.CharField(
        max_length=1, choices=choices, null=True, blank=True)

    def __str__(self) -> str:
        if self.nome_emprestado:
            nome = self.nome_emprestado
        else:
            nome = self.nome_emprestado_anonimo
        return f'{nome} | {self.livro.nome}'

    class Meta:
        verbose_name = 'Emprestimo'
