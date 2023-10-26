from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.postgres.fields import ArrayField
from datetime import date

# Create your models here.
class User(AbstractUser):
    pass

class Consulta(models.Model):

    veterinario = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="consultas")
    raca = models.TextField()
    imagem = models.TextField()
    doenca = models.CharField(max_length = 200)
    probabilidade = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.CharField(max_length = 20, null=True)
    prescricao = models.TextField(max_length = 200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Record ID: {self.id}'
