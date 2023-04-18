# Generated by Django 4.2 on 2023-04-06 01:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0011_remove_livros_data_devolucao_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emprestimos',
            options={'verbose_name': 'Emprestimo'},
        ),
        migrations.RemoveField(
            model_name='emprestimos',
            name='tempo_duracao',
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='data_devolucao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livros',
            name='data_cadastro',
            field=models.DateField(default=datetime.datetime(2023, 4, 6, 1, 43, 35, 940115, tzinfo=datetime.timezone.utc)),
        ),
    ]
