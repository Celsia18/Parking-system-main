# Generated by Django 4.1.3 on 2022-11-13 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('carnumber', models.CharField(max_length=8, verbose_name='Номер Машины')),
                ('date', models.DateField(verbose_name='Дата рождения')),
                ('email', models.CharField(max_length=50, verbose_name='Электронная почта')),
                ('status', models.IntegerField(null=True, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('registration', models.CharField(max_length=50, verbose_name='Логин')),
                ('password', models.CharField(max_length=250, verbose_name='Пароль')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.user')),
            ],
        ),
    ]
