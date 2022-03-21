# Generated by Django 4.0.3 on 2022-03-21 18:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registry', '0008_alter_doctors_firstname_alter_doctors_lastname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(1), to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]