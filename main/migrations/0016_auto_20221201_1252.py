# Generated by Django 3.2.16 on 2022-12-01 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_parkingplacetype_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingplacetype',
            name='is_open',
            field=models.IntegerField(blank=True, choices=[(1, 'Крытое'), (0, 'Открытое')], null=True, verbose_name='Открытое-закрытое'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='is_open',
            field=models.IntegerField(blank=True, choices=[(1, 'Крытое'), (0, 'Открытое')], null=True, verbose_name='Открытое-закрытое'),
        ),
    ]