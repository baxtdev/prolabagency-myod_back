# Generated by Django 5.0.2 on 2024-05-03 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0004_equipmentfavorites_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentfavorites',
            options={'managed': True, 'ordering': ['-id'], 'verbose_name': 'Избранные Оборудовании', 'verbose_name_plural': 'Избранные Оборудовании'},
        ),
    ]
