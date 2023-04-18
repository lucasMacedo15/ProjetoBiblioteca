from django.contrib import admin
from .models import Usuario
# Register your models here.


class AdminUsuario(admin.ModelAdmin):
    list_display = ['nome', 'email', 'senha']
    readonly_fields = ['nome', 'email', 'senha']


admin.site.register(Usuario, AdminUsuario)
