# Generated by Django 3.2.16 on 2022-12-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20221201_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingplacetype',
            name='is_open',
            field=models.BooleanField(choices=[(1, 'Крытое'), (0, 'Открытое')], default=0, verbose_name='Открытое-закрытое'),
        ),
        migrations.AlterField(
            model_name='parkingplacetype',
            name='location',
            field=models.IntegerField(blank=True, choices=[(1, 'Рядом со входом'), (0, 'Рядом с выездом')], null=True, verbose_name='Расположение'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='is_open',
            field=models.BooleanField(blank=True, choices=[(1, 'Крытое'), (0, 'Открытое')], default=0, null=True, verbose_name='Открытое-закрытое'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='location',
            field=models.IntegerField(blank=True, choices=[(1, 'Рядом со входом'), (0, 'Рядом с выездом')], null=True, verbose_name='Расположение'),
        ),
    ]