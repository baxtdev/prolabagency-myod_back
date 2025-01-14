# Generated by Django 5.0.2 on 2024-04-18 12:54

import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apiaries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('order_conditions', models.TextField(verbose_name='Условия заказа')),
                ('delivery_text', models.TextField(verbose_name='Delivery')),
                ('price_for', models.CharField(choices=[('day', 'День'), ('week', 'Неделя'), ('month', 'Месяц')], default='day', max_length=10, verbose_name='Цена за')),
                ('price', models.PositiveBigIntegerField(verbose_name='Цена')),
                ('discount', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Скидка')),
                ('location', models.CharField(max_length=300, verbose_name='Местоположение')),
                ('latitude', models.DecimalField(decimal_places=6, help_text='Укажите северную широту', max_digits=9, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=6, help_text='Укажите восточную долготу', max_digits=9, verbose_name='Долгота')),
                ('take_days_start', models.DateTimeField(blank=True, null=True, verbose_name='Начало')),
                ('take_days_end', models.DateTimeField(blank=True, null=True, verbose_name='Конец')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Популярный')),
                ('is_new', models.BooleanField(default=True, verbose_name='Ноинка')),
                ('raiting', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Рейтинг')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apiaries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пасеки',
                'verbose_name_plural': 'Пасеки',
                'ordering': ['-id', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ApiariesPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=90, scale=None, size=[1920, 1080], upload_to='apiaries/', verbose_name='Фото')),
                ('apiaries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apiaries', to='apiaries.apiaries')),
            ],
            options={
                'verbose_name': 'Фотография Пасеков',
                'verbose_name_plural': 'Фотографии Пасеков',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
