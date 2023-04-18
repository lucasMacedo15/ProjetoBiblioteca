from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import Usuario
from hashlib import sha256
# Create your views here.


class Login(View):
    template_name = 'usuarios/login.html'

    def get(self, request, *args, **kwargs):
        contexto = {'status': self.request.GET.get('status')
                    }

        return render(request, self.template_name, contexto)


class Cadastro(View):
    template_name = 'usuarios/cadastro.html'
    error_messages = {}

    def get(self, request, *args, **kwargs):
        status = self.request.GET.get('status')
        if self.request.session.get('usuario'):
            return redirect('/livro/home/')
        contexto = {
            'status': status,
            'mensagem': None
        }
        if self.error_messages:
            for k, v in self.error_messages.items():
                contexto['mensagem'] = v

        return render(request, self.template_name, contexto)


class ValidaCadastro(Cadastro):

    def post(self, request, *args, **kwargs):
        nome = self.request.POST.get('nome')
        email = self.request.POST.get('email')
        senha = self.request.POST.get('senha')

        usuario = Usuario.objects.filter(email=email).first()
        # Verificações básicas. Intuito educativo
        if len(nome.strip()) == 0 or len(email.strip()) == 0:
            self.error_messages['campo_vazio'] = 'Senha ou nome não devem estar em branco'
            return redirect('/auth/cadastro/?status=1')
        if len(senha) < 2:
            self.error_messages['senha_pequena'] = 'Senha menor que 2 caracteres'
            print('teste')

            return redirect('/auth/cadastro/?status=2')
        if usuario:
            self.error_messages['usuario'] = 'Email já existe'
            return redirect('/auth/cadastro/?status=3')
        try:
            # Utilização de hash para senha
            senha = sha256(senha.encode()).hexdigest()
            usuario = Usuario(nome=nome, email=email, senha=senha)
            usuario.save()
            return redirect('/auth/cadastro/?status=0')
        except:
            self.error_messages['error'] = 'Erro interno do sistema'
            return redirect('/auth/cadastro/status=4')


class ValidaLogin(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha = sha256(senha.encode()).hexdigest()

        usuario = Usuario.objects.filter(email=email, senha=senha).first()

        if not usuario:
            return redirect('/auth/login/?status=1')

        self.request.session['usuario'] = usuario.id

        return redirect(f'/livro/home/?user_id={usuario.id}')


class Sair(View):
    def get(self, request, *args, **kwargs):
        self.request.session.flush()
        return redirect('/auth/login/')
