from django.contrib import admin
from django.urls import path, include
from clientes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.pagina_inicial, name='home'),
    path('clientes/', include('clientes.urls')),
    path('servicos/', include('servicos.urls')),
    path('usuarios/', include('usuarios.urls')),

]
