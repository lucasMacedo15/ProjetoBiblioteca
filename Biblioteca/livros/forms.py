from django import forms
from .models import Livros, Categoria
from django.utils import timezone
from usuarios.models import Usuario
from django.db import models
# Utilização de model form


class CadastroLivro(forms.ModelForm):
    class Meta:
        model = Livros
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()


# Utilizando form
"""
class CadastroLivro(forms.Form):
    nome = forms.CharField(max_length=100)
    autor = forms.CharField(max_length=30)
    co_autor = forms.CharField(max_length=30)
    data_cadastro = forms.DateField()
    emprestado = forms.BooleanField()

"""


class CategoriaLivro(forms.Form):
    nome = forms.CharField(max_length=30)
    descricao = forms.CharField(max_length=60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget = forms.Textarea()
