# Generated by Django 5.0.3 on 2024-04-09 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_e_cadastro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='telefone',
            field=models.IntegerField(),
        ),
    ]
