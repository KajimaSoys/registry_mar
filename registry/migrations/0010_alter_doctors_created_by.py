# Generated by Django 4.0.3 on 2022-03-21 18:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registry', '0009_doctors_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=models.SET(1), to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
    ]
