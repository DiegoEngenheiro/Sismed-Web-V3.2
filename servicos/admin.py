from django.contrib import admin
from .models import CategoriaConsulta, Servico, ServicoAdicional

admin.site.register(CategoriaConsulta)
admin.site.register(Servico)
admin.site.register(ServicoAdicional)