# Generated by Django 5.0.2 on 2024-05-20 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='photo1',
            new_name='photo_1',
        ),
        migrations.RenameField(
            model_name='advertisement',
            old_name='photo2',
            new_name='photo_2',
        ),
    ]
