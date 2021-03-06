# Generated by Django 4.0.4 on 2022-04-19 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_equipement', models.CharField(max_length=50)),
                ('username_ssh', models.CharField(max_length=50)),
                ('password_ssh', models.CharField(max_length=50)),
                ('adresse_ip', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('routeur', 'routeur'), ('switch', 'switch'), ('serveur', 'serveur')], max_length=30)),
                ('systeme', models.CharField(choices=[('windows', 'windows'), ('serveur', 'serveur')], max_length=50)),
            ],
        ),
    ]
