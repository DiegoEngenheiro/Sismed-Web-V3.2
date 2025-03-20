from email.policy import default
from secrets import token_hex, token_urlsafe
from django.db import models
from clientes.models import Cliente
from .choices import ChoicesCategoriaConsulta
from datetime import datetime

class CategoriaConsulta(models.Model):
    titulo = models.CharField(max_length=3, choices=ChoicesCategoriaConsulta.choices)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.titulo

class ServicoAdicional(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField()
    preco = models.FloatField()

    def __str__(self) -> str:
        return self.titulo

class Servico(models.Model):
    titulo = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    categoria_Consulta = models.ManyToManyField(CategoriaConsulta)
    horario = models.TimeField(default='00:00')  # Valor padrão definido aqui
    local = models.CharField(max_length=100, default='Local não informado')  # Valor padrão para local
    protocole = models.CharField(max_length=50, unique=True, blank=True, null=True)
    identificador = models.CharField(max_length=50, unique=True, blank=True, null=True)  
    data_agendada = models.DateField(null=True)
    finalizado = models.BooleanField(default=False)
    servicos_adicionais = models.ManyToManyField(ServicoAdicional)

    def __str__(self) -> str:
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.protocole:
            self.protocole = datetime.now().strftime("%d/%m/%Y-%H:%M:%S-") + token_hex(16)

        if not self.identificador:
            self.identificador = token_urlsafe(16)

        super(Servico, self).save(*args, **kwargs)

    def preco_total(self):
        preco_total = float(0)
        for categoria in self.categoria_Consulta.all():
            preco_total += float(categoria.preco)

        return preco_total
    