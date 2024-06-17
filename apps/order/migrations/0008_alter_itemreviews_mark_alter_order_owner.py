# Generated by Django 5.0.2 on 2024-05-20 11:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_code_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemreviews',
            name='mark',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
