# Generated by Django 5.0.3 on 2024-09-25 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0005_process_end_info_process_start_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='end_info',
        ),
        migrations.RemoveField(
            model_name='process',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='process',
            name='start_info',
        ),
        migrations.RemoveField(
            model_name='process',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='process',
            name='main_process',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='process',
            name='sub_process',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='TimeInterval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_info', models.TextField(blank=True, null=True)),
                ('end_info', models.TextField(blank=True, null=True)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_intervals', to='timeintervals.process')),
            ],
        ),
    ]
