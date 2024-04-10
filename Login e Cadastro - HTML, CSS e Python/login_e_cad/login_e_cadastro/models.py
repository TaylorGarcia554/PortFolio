from django.db import models

class usuarios(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    telefone = models.IntegerField()
    senha = models.TextField(max_length=50)

