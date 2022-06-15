# Generated by Django 4.0.4 on 2022-04-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('data_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('type_operation', models.CharField(max_length=20)),
                ('nom_utilisateur', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('data_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('type_operation', models.CharField(max_length=20)),
                ('nom_utilisateur', models.CharField(max_length=20)),
                ('equipements', models.CharField(max_length=200)),
                ('procedure', models.CharField(max_length=1000)),
            ],
        ),
    ]