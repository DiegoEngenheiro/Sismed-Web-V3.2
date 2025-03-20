from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('atualiza_cliente/', views.att_cliente, name="atualiza_cliente"),
    path('consultar_cliente/', views.consultar_cliente, name='consultar_cliente'),
    path('update_cliente/<int:id>', views.update_cliente, name="update_cliente")
]