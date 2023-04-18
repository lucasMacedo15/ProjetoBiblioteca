from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.Login.as_view(), name='login'),
    path('cadastro/', views.Cadastro.as_view(), name='cadastro'),
    path('valida_cadastro/', views.ValidaCadastro.as_view(), name='valida_cadastro'),
    path('valida_login/', views.ValidaLogin.as_view(), name='valida_login'),
    path('sair/', views.Sair.as_view(), name='sair'),
]
