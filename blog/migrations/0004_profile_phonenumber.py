# Generated by Django 4.2.6 on 2024-03-27 03:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_profile_image_remove_profile_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phoneNumber',
            field=models.CharField(max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
