# Generated by Django 4.2.1 on 2023-06-10 20:02

import django.db.models.deletion
from django.db import (
    migrations,
    models
)


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155, verbose_name='Название')),
                ('description', models.CharField(max_length=500, verbose_name='Описание')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'К выполнению'), (2, 'В процессе'), (3, 'Готово'), (4, 'В архиве')], default=1, verbose_name='Статус')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий'), (4, 'Критический')], default=2, verbose_name='Приоритет')),
                ('deadline', models.DateTimeField(verbose_name='Дата дедлайна')),
                ('created', models.DateTimeField(verbose_name='Дата создания')),
                ('updated', models.DateTimeField(verbose_name='Дата последнего обновления')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goalcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Цель',
                'verbose_name_plural': 'Цели',
            },
        ),
    ]
