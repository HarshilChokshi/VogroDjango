# Generated by Django 3.0.5 on 2020-05-07 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vogro_api', '0007_matchedtask'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='client_number',
            field=models.CharField(default=2263788998, max_length=20),
            preserve_default=False,
        ),
    ]
