# Generated by Django 5.0.3 on 2024-03-16 05:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_customer_seller_customuser_type_customeradditional_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=5)),
                ('phone', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='phone number should exactly be in 10 digits', regex='^\\d{10}$')])),
                ('query', models.TextField()),
            ],
        ),
    ]
