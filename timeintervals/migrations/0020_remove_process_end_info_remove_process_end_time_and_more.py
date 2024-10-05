# Generated by Django 5.0.3 on 2024-09-26 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0019_delete_interval'),
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
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('start_info', models.CharField(blank=True, max_length=100, null=True)),
                ('end_info', models.CharField(blank=True, max_length=100, null=True)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to='timeintervals.process')),
            ],
        ),
    ]
