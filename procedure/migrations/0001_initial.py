# Generated by Django 4.0.4 on 2022-04-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=300)),
                ('type_equipement', models.CharField(max_length=20)),
                ('systeme', models.CharField(max_length=300)),
            ],
        ),
    ]
