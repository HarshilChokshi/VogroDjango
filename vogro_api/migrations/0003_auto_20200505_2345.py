# Generated by Django 3.0.5 on 2020-05-05 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vogro_api', '0002_clientuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientuser',
            name='address_name',
            field=models.CharField(max_length=70),
        ),
    ]
