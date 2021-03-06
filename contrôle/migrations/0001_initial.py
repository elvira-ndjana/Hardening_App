# Generated by Django 4.0.4 on 2022-04-30 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('procedure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('libelle', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=300)),
                ('default', models.BooleanField(max_length=10)),
                ('commande', models.CharField(max_length=10000)),
                ('procedure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='procedure.procedure')),
            ],
        ),
    ]
