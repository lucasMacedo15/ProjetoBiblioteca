from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import View, TemplateView, DetailView
from .models import Livros, Categoria, Emprestimos
from usuarios.models import Usuario
from utils import subtrai
from .forms import CadastroLivro, CategoriaLivro
# Create your views here.
from django.utils import timezone
from copy import deepcopy


class Home(View):
    template_name = 'livros/home.html'

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.id_usuario = self.request.session.get('usuario')
        form = CadastroLivro()
        form_categoria = CategoriaLivro()
        usuarios = Usuario.objects.all().exclude(id=self.id_usuario)
        livros_usuario = Livros.objects.filter(usuario_id=self.id_usuario)
        livros_nao_emprestados = Livros.objects.filter(
            usuario_id=self.id_usuario).filter(emprestado=False)
        livros_emprestados = Livros.objects.filter(
            usuario_id=self.id_usuario).filter(emprestado=True)
        # Arrumar livro emprestado
        form.fields['categoria'].queryset = Categoria.objects.filter(
            usuario_id=self.id_usuario)
        form.fields['categoria'].queryset
        self.contexto = {'usuario_logado': self.id_usuario,
                         'form': form,
                         'form_categoria_livro': form_categoria,
                         'usuarios': usuarios,
                         'livros': livros_usuario,
                         'livros_nao_emprestados': livros_nao_emprestados,
                         'livros_emprestados': livros_emprestados,
                         }

    def get(self, request, *args, **kwargs):
        if not self.id_usuario:
            return redirect('/auth/login/?status=2')
        # status = {'mensagem': 'Teste'}

        return render(request, self.template_name, self.contexto)


class VerLivro(Home):
    template_name = 'livros/detalhes.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:

        self.livro = Livros.objects.get(id=kwargs.get('id'))
        categorias = Categoria.objects.filter(usuario_id=self.id_usuario)
        emprestimos = Emprestimos.objects.filter(livro_id=self.livro)

        if not self.id_usuario:
            return redirect('/auth/login/')

        if self.livro.usuario.id != self.id_usuario:
            return redirect('/livro/home/')

        contexto = {'livro': self.livro, 'categorias': categorias,
                    'emprestimos': emprestimos}
        contexto.update(self.contexto)

        return render(request, self.template_name, contexto)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        http_referer = self.request.META.get('HTTP_REFERER')

        return redirect(http_referer)


class CadastrarLivro(Home):

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = CadastroLivro(self.request.POST, self.request.FILES)

        usuario = Usuario.objects.get(id=self.id_usuario)
        new_form = deepcopy(form.data)
        new_form['usuario'] = usuario
        form.data = new_form
        imagem = self.request.FILES.get('img')
        form.save()

        if not form.is_valid():
            return HttpResponse('Formularia não é válido')

        return HttpResponse('Cadastrando lviro')


class ExcluirLivro(VerLivro):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if not self.livro.usuario.id == self.id_usuario:

            return HttpResponse('ESte livro nao pertence a este usuário')
        self.livro.delete()
        return redirect('/livro/home/')


class CadastrarCategoria(Home):

    def post(self, request, *args, **kwargs) -> HttpResponse:
        super().get(request, *args, **kwargs)

        form_categoria = CategoriaLivro(self.request.POST)
        nome = form_categoria['nome'].data
        descricao = form_categoria['descricao'].data

        categoria_db = Categoria(
            nome=nome, descricao=descricao, usuario_id=self.id_usuario)

        categoria_db.save()

        return redirect('/livro/home/')


class CadastrarEmprestimo(Home):
    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        usuario_cadastrado = self.request.POST.get('usuario_cadastrado')
        usuario_anonimo = self.request.POST.get('usuario_anonimo')
        livro_emprestado = self.request.POST.get('livro_emprestado')
        usuario_origem = Usuario.objects.get(id=self.id_usuario)

        # Consertar o BUG aqui
        # if usuario_anonimo and usuario_cadastrado:
        #     return HttpResponse('Não pode fazer isto')
        if usuario_anonimo:
            usuario_cadastrado = None

        emprestimo = Emprestimos(nome_emprestado_id=usuario_cadastrado,
                                 nome_emprestado_anonimo=usuario_anonimo,
                                 livro_id=livro_emprestado,
                                 data_devolucao=None
                                 )

        livro = Livros.objects.get(id=livro_emprestado)
        livro.emprestado = True
        livro.save()
        emprestimo.save()
        # Adicionar msg de emprestimo com sucesso
        return redirect('/livro/home/')


class DevolverLivro(View):

    def post(self, request, *args, **kwargs):

        id_livro = self.request.POST.get('livro_devolvido')
        livro = Livros.objects.get(id=id_livro)
        livro.emprestado = False

        emprestimo = livro.emprestimos_set.all().filter(livro_id=id_livro).last()

        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()
        livro.save()
        return HttpResponse('devolvido')


class AlterarLivro(Home):

    def post(self, request, *args, **kwargs):
        id_livro = self.request.POST.get('livro_id')
        nome_livro = self.request.POST.get('nome_livro')
        autor = self.request.POST.get('autor')
        co_autor = self.request.POST.get('co_autor')
        categoria = self.request.POST.get('categoria')
        livro = get_object_or_404(Livros, id=id_livro, usuario=self.id_usuario)
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        nova_cat = Categoria.objects.get(id=categoria)
        livro.categoria = nova_cat

        livro.save()

        return redirect(f'/livro/ver_livro/{id_livro}')


class SeusEmprestimos(Home):
    template_name = 'livros/seus_emprestimos.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.contexto['livros_emprestados'] = Emprestimos.objects.filter(
            nome_emprestado_id=self.id_usuario)

        print(self.contexto['livros_emprestados'])
        return render(request, self.template_name, self.contexto)


class ProcessaAvaliacao(VerLivro):
    def post(self, request, *args, **kwargs) -> HttpResponse:
        id_emprestimo = self.request.POST.get('id_emprestimo')
        id_livro = self.request.POST.get('id_livro')
        opcao = self.request.POST.get('opcoes')

        emprestimo = Emprestimos.objects.get(id=id_emprestimo)
        emprestimo.avaliacao = opcao
        if self.id_usuario != emprestimo.livro.usuario.id:
            # INSERIR MENSAGEM DE ERRO
            # Não pode fazer avaliação de outro usuário
            return redirect(f'/livro/ver_livro/{id_livro}')

        emprestimo.save()
        return redirect(f'/livro/ver_livro/{id_livro}')
