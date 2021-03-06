# Generated by Django 4.0.3 on 2022-03-16 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='free',
            field=models.BooleanField(default=True, verbose_name='Свободен?'),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
        migrations.AlterField(
            model_name='doctortypes',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
        migrations.AlterField(
            model_name='exempts',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
        migrations.AlterField(
            model_name='medcards',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
        migrations.AlterField(
            model_name='medcards',
            name='sign',
            field=models.BooleanField(default=False, verbose_name='Работник предприятия?'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
        migrations.AlterField(
            model_name='services',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
        migrations.AlterField(
            model_name='talons',
            name='close',
            field=models.BooleanField(default=False, verbose_name='Закрыт?'),
        ),
        migrations.AlterField(
            model_name='talons',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Активен?'),
        ),
    ]
