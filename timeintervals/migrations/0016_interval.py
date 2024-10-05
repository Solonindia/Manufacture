# Generated by Django 5.0.3 on 2024-09-26 06:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0015_process_end_info_process_start_info_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_info', models.CharField(blank=True, max_length=100, null=True)),
                ('end_info', models.CharField(blank=True, max_length=100, null=True)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to='timeintervals.process')),
            ],
        ),
    ]
