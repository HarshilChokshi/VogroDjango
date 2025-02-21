# Generated by Django 3.0.5 on 2020-05-09 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vogro_api', '0009_completedtask'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnMatchedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_location', models.TextField()),
                ('description', models.CharField(max_length=50)),
                ('task_type', models.CharField(max_length=30)),
                ('client_name', models.CharField(max_length=30)),
                ('client_number', models.CharField(max_length=20)),
                ('earliest_preferred_time', models.DateTimeField()),
                ('latest_preferred_time', models.DateTimeField()),
            ],
        ),
    ]
