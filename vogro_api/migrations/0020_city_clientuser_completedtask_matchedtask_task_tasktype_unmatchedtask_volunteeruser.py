# Generated by Django 3.0.5 on 2020-05-22 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vogro_api', '0019_auto_20200522_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('address_name', models.CharField(max_length=100)),
                ('reason', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('task_type', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='VolunteerUser',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=25)),
                ('is_verified', models.BooleanField(default=False)),
                ('has_used_app', models.BooleanField(default=False)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.City')),
            ],
        ),
        migrations.CreateModel(
            name='UnMatchedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_location', models.TextField()),
                ('description', models.TextField()),
                ('client_name', models.CharField(max_length=30)),
                ('client_email', models.CharField(max_length=50)),
                ('client_number', models.CharField(max_length=20)),
                ('earliest_preferred_time', models.DateTimeField()),
                ('latest_preferred_time', models.DateTimeField()),
                ('estimated_time', models.CharField(max_length=20)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.City')),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.TaskType')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_location', models.TextField()),
                ('description', models.TextField()),
                ('client_name', models.CharField(max_length=30)),
                ('client_email', models.CharField(max_length=50)),
                ('client_number', models.CharField(max_length=20)),
                ('earliest_preferred_time', models.DateTimeField()),
                ('latest_preferred_time', models.DateTimeField()),
                ('estimated_time', models.CharField(max_length=20)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.City')),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.TaskType')),
            ],
        ),
        migrations.CreateModel(
            name='MatchedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_location', models.TextField()),
                ('description', models.TextField()),
                ('client_name', models.CharField(max_length=30)),
                ('client_email', models.CharField(max_length=50)),
                ('client_number', models.CharField(max_length=20)),
                ('earliest_preferred_time', models.DateTimeField()),
                ('latest_preferred_time', models.DateTimeField()),
                ('estimated_time', models.CharField(max_length=20)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.City')),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.TaskType')),
                ('volunteer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.VolunteerUser')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_location', models.TextField()),
                ('description', models.TextField()),
                ('client_name', models.CharField(max_length=30)),
                ('client_email', models.CharField(max_length=50)),
                ('client_number', models.CharField(max_length=20)),
                ('earliest_preferred_time', models.DateTimeField()),
                ('latest_preferred_time', models.DateTimeField()),
                ('estimated_time', models.CharField(max_length=20)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.City')),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.TaskType')),
                ('volunteer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vogro_api.VolunteerUser')),
            ],
        ),
    ]
