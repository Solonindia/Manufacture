# Generated by Django 5.0.3 on 2024-11-19 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0004_mainprocess_end_time_mainprocess_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainprocess',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='mainprocess',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='subprocess',
            name='additional_info',
        ),
        migrations.RemoveField(
            model_name='subprocess',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='subprocess',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='mainprocess',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='ProductionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('time_slot', models.TimeField()),
                ('main_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.mainprocess')),
                ('sub_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.subprocess')),
            ],
        ),
    ]
