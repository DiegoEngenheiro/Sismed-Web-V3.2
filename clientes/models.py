from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    cpf = models.CharField(max_length=12)
    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)  # Verifique se este campo existe


    def __str__(self) -> str:
        return self.nome
    