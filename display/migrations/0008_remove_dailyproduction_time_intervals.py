# Generated by Django 5.0.3 on 2024-09-20 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0007_alter_dailyproduction_time_intervals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyproduction',
            name='time_intervals',
        ),
    ]
