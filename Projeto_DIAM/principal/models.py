from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #id = models.AutoField(primary_key=True)
    #nome_utilizador = models.CharField(max_length=30)
    #email = models.EmailField()
    telefone = models.CharField(max_length=9)
    #password = models.CharField(max_length=40)
    ativo = models.BooleanField(default=False) #ver se vale a pena ter ou se apagamos
    #criador = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True) #confirmar se posso meter null=false e depois
    acesso = models.IntegerField(default=1) #default = chefe

class Medidas(models.Model):
    medidas_id = models.AutoField(primary_key=True)
    medidas_nome = models.CharField(max_length=30)

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    categoria_nome = models.CharField(max_length=30)
    categoria_medida=models.ForeignKey(Medidas, on_delete=models.CASCADE, related_name='categorias')
    #categoria_admin = models.ForeignKey(Administrador) - o tiago nao quer

class Ingrediente(models.Model):
    ingrediente_id = models.AutoField(primary_key=True)
    ingrediente_nome = models.CharField(max_length=30)
    ingrediente_categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='ingredientes')
    ingrediente_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # only admin
    ingrediente_imagem = models.FileField(upload_to='principal/static/imagens/ingredientes/', blank=True, null=True)


class Receita(models.Model):
    receita_id = models.AutoField(primary_key=True)
    receita_nome = models.CharField(max_length=30)
    receita_descricao = models.CharField(max_length=1000)
    receita_tempo_confecao = models.IntegerField()
    receita_imagem = models.FileField(upload_to='principal/static/imagens/receita/', blank=True, null=True)
    receita_user = models.ForeignKey(User, on_delete=models.CASCADE)

class ReceitaIngrediente(models.Model):
    receita = models.ForeignKey('Receita', on_delete=models.CASCADE)
    ingrediente = models.ForeignKey('Ingrediente', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
class Armario(models.Model):
    armario_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    armario_ingredientes = models.ManyToManyField(Ingrediente)
