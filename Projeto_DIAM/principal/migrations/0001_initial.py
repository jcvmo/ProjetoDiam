# Generated by Django 5.0.4 on 2024-05-03 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]


    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_nome_utilizador', models.CharField(max_length=30)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_telefone', models.CharField(max_length=9)),
                ('user_password', models.CharField(max_length=40)),
                ('user_ativo', models.BooleanField(default=False)),
                ('user_criador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='principal.user')),
                ('user_acesso', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Medidas',
            fields=[
                ('medidas_id', models.AutoField(primary_key=True, serialize=False)),
                ('medidas_nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('categoria_id', models.AutoField(primary_key=True, serialize=False)),
                ('categoria_nome', models.CharField(max_length=30)),
                ('categoria_medida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='principal.medidas')),
            ],
        ),
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('ingrediente_id', models.AutoField(primary_key=True, serialize=False)),
                ('ingrediente_nome', models.CharField(max_length=30)),
                ('ingrediente_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientes', to='principal.categoria')),
                ('ingrediente_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='principal.user')),
                ('ingrediente_imagem', models.FileField(blank=True, null=True, upload_to='ingredientes/')),
                ('ingrediente_quantidade', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Armario',
            fields=[
                ('armario_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='principal.user')),
                ('armario_ingredientes', models.ManyToManyField(to='principal.ingrediente')),
            ],
        ),
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('receita_id', models.AutoField(primary_key=True, serialize=False)),
                ('receita_nome', models.CharField(max_length=30)),
                ('receita_descricao', models.CharField(max_length=1000)),
                ('receita_tempo_confecao', models.IntegerField()),
                ('receita_imagem', models.FileField(blank=True, null=True, upload_to='receita/')),
                ('receita_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.user')),
                ('ingredientes', models.ManyToManyField(to='principal.ingrediente')),
            ],
        ),
    ]
