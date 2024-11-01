# Generated by Django 5.0.3 on 2024-09-25 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0007_process_end_info_process_end_time_process_start_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='end_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='process',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='process',
            name='main_process',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='process',
            name='start_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='process',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='process',
            name='sub_process',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_info', models.TextField(blank=True, null=True)),
                ('end_info', models.TextField(blank=True, null=True)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to='timeintervals.process')),
            ],
        ),
    ]
