from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.Home.as_view(), name='home'),
    path('ver_livro/<int:id>', views.VerLivro.as_view(), name='ver_livro'),
    path('cadastrar_livro/', views.CadastrarLivro.as_view(), name='cadastrar_livro'),
    path('excluir_livro/<int:id>',
         views.ExcluirLivro.as_view(), name='excluir_livro'),
    path('cadastrar_categoria/', views.CadastrarCategoria.as_view(),
         name='cadastrar_categoria'),
    path('cadastrar_emprestimo/', views.CadastrarEmprestimo.as_view(),
         name='cadastrar_emprestimo'),
    path('devolver_livro/', views.DevolverLivro.as_view(),
         name='devolver_livro'),
    path('alterar_livro/<int:id>', views.AlterarLivro.as_view(),
         name='alterar_livro'),
    path('seus_emprestimos/', views.SeusEmprestimos.as_view(),
         name='seus_emprestimos'),
    path('processa_avaliacao/', views.ProcessaAvaliacao.as_view(),
         name='processa_avaliacao'),

]
