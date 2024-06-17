# Generated by Django 5.0.2 on 2024-04-19 09:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiaries', '0002_alter_apiariesphotos_apiaries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiaries',
            name='take_days_end',
        ),
        migrations.RemoveField(
            model_name='apiaries',
            name='take_days_start',
        ),
        migrations.CreateModel(
            name='BookedDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('start_day', models.DateTimeField(blank=True, null=True, verbose_name='Начало')),
                ('end_day', models.DateTimeField(blank=True, null=True, verbose_name='Конец')),
                ('apiaries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_days', to='apiaries.apiaries')),
            ],
            options={
                'verbose_name': 'Забронированные дни',
                'verbose_name_plural': 'Забронированные дни',
                'db_table': '',
                'managed': True,
            },
        ),
    ]