# Generated by Django 4.2.1 on 2023-06-13 15:04

import django.db.models.deletion
from django.db import (
    migrations,
    models
)


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_create_new_objects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalcategory',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='goals.board', verbose_name='Доска'),
        ),
    ]
