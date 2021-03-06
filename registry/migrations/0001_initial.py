# Generated by Django 4.0.3 on 2022-03-16 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('lastname', models.CharField(max_length=20, verbose_name='Имя')),
                ('firstname', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=20, verbose_name='Отчество')),
                ('university', models.CharField(max_length=100, verbose_name='Университет')),
                ('experience', models.IntegerField(verbose_name='Опыт работы')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('born', models.DateField(verbose_name='Год рождения')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
            ],
            options={
                'verbose_name': 'Доктор',
                'verbose_name_plural': 'Доктора',
            },
        ),
        migrations.CreateModel(
            name='DoctorTypes',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=100, verbose_name='Специализация')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
            ],
            options={
                'verbose_name': 'Специализация',
                'verbose_name_plural': 'Специализации',
            },
        ),
        migrations.CreateModel(
            name='Exempts',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('exempttype', models.CharField(max_length=50, verbose_name='Льгота')),
                ('exempt', models.IntegerField(verbose_name='Сумма льготы')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
            ],
            options={
                'verbose_name': 'Льгота',
                'verbose_name_plural': 'Льготы',
            },
        ),
        migrations.CreateModel(
            name='Medcards',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('fio', models.CharField(max_length=100, verbose_name='ФИО')),
                ('number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес')),
                ('district', models.CharField(max_length=50, verbose_name='Район')),
                ('policynumber', models.CharField(max_length=10, verbose_name='Номер медицинского полиса')),
                ('year', models.SmallIntegerField(verbose_name='Год рождения')),
                ('sign', models.BooleanField(verbose_name='Работник предприятия?')),
                ('department', models.CharField(blank=True, max_length=30, verbose_name='Отдел, в котороом работает')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
                ('exemptid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ExemptID', to='registry.exempts', verbose_name='Льгота')),
            ],
            options={
                'verbose_name': 'Медицинская карта',
                'verbose_name_plural': 'Медицинские карты',
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('number', models.IntegerField(verbose_name='Номер кабинета')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
            ],
            options={
                'verbose_name': 'Кабинет',
                'verbose_name_plural': 'Кабинеты',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=100, verbose_name='Название услуги')),
                ('cost', models.IntegerField(verbose_name='Стоимость услуги')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Shedule',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('date', models.DateField(verbose_name='Дата')),
                ('start', models.TimeField(verbose_name='Работает с')),
                ('end', models.TimeField(verbose_name='Работает до')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RoomID', to='registry.rooms', verbose_name='Кабинет')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
            },
        ),
        migrations.CreateModel(
            name='Talons',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('datestart', models.DateField(verbose_name='Дата посещения')),
                ('timestart', models.TimeField(verbose_name='Время посещения')),
                ('close', models.BooleanField(verbose_name='Закрыт?')),
                ('comment', models.TextField(verbose_name='Примечания (результаты приема)')),
                ('cost', models.IntegerField(default=0, verbose_name='Стоимость услуг')),
                ('summa', models.IntegerField(default=0, verbose_name='К оплате')),
                ('enabled', models.BooleanField(verbose_name='Активен?')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.doctors', verbose_name='Доктор')),
                ('mcid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MCID', to='registry.medcards', verbose_name='Карточка пациента')),
                ('service', models.ManyToManyField(to='registry.services', verbose_name='Услуги')),
                ('sheduleid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SheduleID', to='registry.shedule', verbose_name='Расписание')),
            ],
            options={
                'verbose_name': 'Запись на прием',
                'verbose_name_plural': 'Записи на прием',
            },
        ),
        migrations.AddField(
            model_name='doctors',
            name='schedule',
            field=models.ManyToManyField(to='registry.shedule', verbose_name='Открытые даты для посещения'),
        ),
        migrations.AddField(
            model_name='doctors',
            name='typeid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TypeID', to='registry.doctortypes', verbose_name='Специализация'),
        ),
    ]
