# Generated by Django 3.1.4 on 2021-01-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20210107_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messcont',
            name='subject',
            field=models.CharField(max_length=100, verbose_name='Тема сообщения'),
        ),
    ]
