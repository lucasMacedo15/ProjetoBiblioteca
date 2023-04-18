# Generated by Django 4.2 on 2023-04-12 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0014_alter_emprestimos_data_devolucao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimos',
            name='avaliacao',
            field=models.CharField(blank=True, choices=[('P', 'Péssimo'), ('R', 'Ruim'), ('B', 'Bom'), ('O', 'Ótimo')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='data_devolucao',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 12, 20, 37, 50, 848343, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 12, 20, 37, 50, 848343, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='livros',
            name='data_cadastro',
            field=models.DateField(default=datetime.datetime(2023, 4, 12, 20, 37, 50, 847343, tzinfo=datetime.timezone.utc)),
        ),
    ]
