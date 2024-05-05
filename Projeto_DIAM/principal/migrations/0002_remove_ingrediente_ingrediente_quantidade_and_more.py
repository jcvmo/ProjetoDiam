# Generated by Django 5.0.4 on 2024-05-05 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingrediente',
            name='ingrediente_quantidade',
        ),
        migrations.RemoveField(
            model_name='receita',
            name='ingredientes',
        ),
        migrations.CreateModel(
            name='ReceitaIngrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.ingrediente')),
                ('receita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.receita')),
            ],
        ),
    ]
