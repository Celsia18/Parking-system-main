# Generated by Django 3.2.16 on 2022-12-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20221201_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingplacetype',
            name='location',
            field=models.IntegerField(blank=True, choices=[(1, 'Рядом со входом'), (0, 'Рядом с выездом')], null=True, verbose_name='Расположение'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='location',
            field=models.IntegerField(blank=True, choices=[(1, 'Рядом со входом'), (0, 'Рядом с выездом')], null=True, verbose_name='Расположение'),
        ),
    ]
