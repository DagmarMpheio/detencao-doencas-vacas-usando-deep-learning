# Generated by Django 4.2.6 on 2023-10-27 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0004_alter_consulta_probabilidade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consulta",
            name="probabilidade",
            field=models.CharField(max_length=5),
        ),
    ]
