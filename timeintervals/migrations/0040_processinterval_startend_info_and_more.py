# Generated by Django 5.0.3 on 2024-11-21 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0039_rename_additional_info_process_add_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='processinterval',
            name='startend_info',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='processinterval1',
            name='startend_info',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]