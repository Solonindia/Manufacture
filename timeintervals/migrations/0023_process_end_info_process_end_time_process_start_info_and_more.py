# Generated by Django 5.0.3 on 2024-09-26 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0022_remove_process_end_info_remove_process_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='end_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='start_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.DeleteModel(
            name='TimeInterval',
        ),
    ]
