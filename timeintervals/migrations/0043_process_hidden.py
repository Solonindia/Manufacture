# Generated by Django 5.0.3 on 2024-11-22 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0042_remove_process_is_hidden_in_second'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
