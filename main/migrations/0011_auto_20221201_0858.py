# Generated by Django 3.2.16 on 2022-12-01 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_log'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'verbose_name_plural': 'Логи'},
        ),
        migrations.AlterModelOptions(
            name='parking',
            options={'verbose_name_plural': 'Парковки'},
        ),
        migrations.AlterModelOptions(
            name='parkingplace',
            options={'verbose_name_plural': 'Парковочные места'},
        ),
        migrations.AlterModelOptions(
            name='parkingplacestatus',
            options={'verbose_name_plural': 'Статусы парковочных мест'},
        ),
        migrations.AlterModelOptions(
            name='parkingplacetype',
            options={'verbose_name_plural': 'Типы парковочных мест'},
        ),
        migrations.AlterModelOptions(
            name='preferences',
            options={'verbose_name_plural': 'Предпочтение пользователей'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Профили'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'Вопросы'},
        ),
        migrations.RemoveField(
            model_name='parkingplacetype',
            name='is_cover',
        ),
        migrations.RemoveField(
            model_name='parkingplacetype',
            name='is_near_enter',
        ),
        migrations.RemoveField(
            model_name='parkingplacetype',
            name='is_near_exit',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='is_cover',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='is_near_enter',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='is_near_exit',
        ),
        migrations.AddField(
            model_name='parkingplacetype',
            name='location',
            field=models.IntegerField(blank=True, choices=[(0, 'Рядом с выездом'), (1, 'Рядом со входом')], null=True, verbose_name='Расположение'),
        ),
        migrations.AddField(
            model_name='preferences',
            name='location',
            field=models.IntegerField(blank=True, choices=[(0, 'Рядом с выездом'), (1, 'Рядом со входом')], null=True, verbose_name='Расположение'),
        ),
        migrations.AlterField(
            model_name='parkingplacetype',
            name='is_open',
            field=models.BooleanField(choices=[(0, 'Открытое'), (1, 'Крытое')], default=0, verbose_name='Открытое-закрытое'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='is_open',
            field=models.BooleanField(choices=[(0, 'Открытое'), (1, 'Крытое')], default=0, verbose_name='Открытое-закрытое'),
        ),
    ]