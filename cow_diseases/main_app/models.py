from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import ArrayField
from datetime import date

# Create your models here.


class User(AbstractUser):
    telefone = models.CharField(max_length=9, null=True)
    data_nascimento = models.DateField(null=True)
    genero = models.CharField(max_length=20,null=True)
    endereco = models.TextField(max_length=100, null=True)
    fb_link = models.CharField(max_length=250, null=True)
    twitter_link = models.CharField(max_length=250, null=True)
    tiktok_link = models.CharField(max_length=250, null=True)
    instagram_link = models.CharField(max_length=250, null=True)
    bio = models.TextField(null=True)


class Consulta(models.Model):

    veterinario = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="consultas")
    raca = models.TextField()
    imagem = models.TextField()
    doenca = models.CharField(max_length=200)
    probabilidade = models.CharField(max_length=5)
    status = models.CharField(max_length=20, null=True)
    prescricao = models.TextField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Record ID: {self.id}'
