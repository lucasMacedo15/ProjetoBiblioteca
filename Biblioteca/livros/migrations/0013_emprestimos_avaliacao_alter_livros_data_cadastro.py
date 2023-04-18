# Generated by Django 4.2 on 2023-04-12 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0012_alter_emprestimos_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimos',
            name='avaliacao',
            field=models.CharField(choices=[('P', 'Péssimo'), ('R', 'Ruim'), ('B', 'Bom'), ('O', 'Ótimo')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='livros',
            name='data_cadastro',
            field=models.DateField(default=datetime.datetime(2023, 4, 12, 20, 9, 1, 401238, tzinfo=datetime.timezone.utc)),
        ),
    ]
