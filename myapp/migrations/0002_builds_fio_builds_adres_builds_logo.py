# Generated by Django 4.1.7 on 2023-05-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='builds',
            name='FIO',
            field=models.CharField(blank=True, max_length=300, verbose_name='ФИО директора'),
        ),
        migrations.AddField(
            model_name='builds',
            name='adres',
            field=models.TextField(blank=True, max_length=50, verbose_name='Фактический адрес'),
        ),
        migrations.AddField(
            model_name='builds',
            name='logo',
            field=models.ImageField(blank=True, help_text='Логотип организации', upload_to='images/', verbose_name='Логотип'),
        ),
    ]
