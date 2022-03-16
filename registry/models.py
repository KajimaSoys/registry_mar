from django.db import models


class DoctorTypes(models.Model):
    """Модель врачебных специализаций"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    name = models.CharField(verbose_name='Специализация', max_length=100)
    enabled = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Doctors(models.Model):
    """Модель докторов"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    lastname = models.CharField(verbose_name='Имя', max_length=20)
    firstname = models.CharField(verbose_name='Фамилия', max_length=20)
    patronymic = models.CharField(verbose_name='Отчество', max_length=20)
    university = models.CharField(verbose_name='Университет', max_length=100)
    experience = models.IntegerField(verbose_name='Опыт работы')
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    born = models.DateField(verbose_name='Год рождения')
    typeid = models.ForeignKey(DoctorTypes, models.CASCADE, 'TypeID', verbose_name='Специализация')
    schedule = models.ManyToManyField('Schedule', verbose_name='Открытые даты для посещения')
    enabled = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return self.lastname

    def get_fullname(self):
        return f'{self.lastname} {self.firstname} {self.patronymic}'

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'


class Exempts(models.Model):
    """Модель льготы"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    exempttype = models.CharField(verbose_name='Льгота', max_length=50)
    exempt = models.IntegerField(verbose_name='Сумма льготы')
    enabled = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return self.exempttype

    class Meta:
        verbose_name = 'Льгота'
        verbose_name_plural = 'Льготы'


class Medcards(models.Model):
    """Модель мед карт"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    fio = models.CharField(verbose_name='ФИО', max_length=100)
    number = models.CharField(verbose_name='Номер телефона', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=150)
    district = models.CharField(verbose_name='Район', max_length=50)
    policynumber = models.CharField(verbose_name='Номер медицинского полиса', max_length=10)
    year = models.SmallIntegerField(verbose_name='Год рождения')
    sign = models.BooleanField(verbose_name='Работник предприятия?', default=False)
    department = models.CharField(verbose_name='Отдел, в котороом работает', max_length=30, blank=True)
    enabled = models.BooleanField(verbose_name='Активен?', default=True)
    exemptid = models.ForeignKey(Exempts, models.CASCADE, 'ExemptID', verbose_name='Льгота', blank=True, null=True)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Медицинская карта'
        verbose_name_plural = 'Медицинские карты'


class Rooms(models.Model):
    """Модель кабинетов"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    number = models.IntegerField(verbose_name='Номер кабинета')
    enabled = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class Services(models.Model):
    """Модель услуг"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    name = models.CharField(verbose_name='Название услуги', max_length=100)
    cost = models.IntegerField(verbose_name='Стоимость услуги')
    enabled = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Schedule(models.Model):
    """Модель расписаний"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    date = models.DateField(verbose_name='Дата')
    start = models.TimeField(verbose_name='Работает с')
    end = models.TimeField(verbose_name='Работает до')
    # doctorid = models.ManyToManyField(Doctors, 'DoctorID', verbose_name='Доктор')
    roomid = models.ForeignKey(Rooms, models.CASCADE, 'RoomID', verbose_name='Кабинет')  #Под вопросом, возможно, что стоит перекинуть на модель доктора
    free = models.BooleanField(verbose_name='Свободен?', default=True)
    enabled = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return f'{self.date} - ({self.start}-{self.end})'  # ИЗМЕНИТЬ!

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class Talons(models.Model):
    """Модель записей на прием"""
    id = models.BigAutoField(primary_key=True, verbose_name='id')
    mcid = models.ForeignKey(Medcards, models.CASCADE, verbose_name='Карточка пациента')
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, verbose_name='Доктор')
    scheduleid = models.ForeignKey(Schedule, models.CASCADE, verbose_name='Расписание')
    datestart = models.DateField(verbose_name='Дата посещения')
    timestart = models.TimeField(verbose_name='Время посещения')
    service = models.ManyToManyField(Services, verbose_name="Услуги")
    close = models.BooleanField(verbose_name='Закрыт?', default=False)
    comment = models.TextField(verbose_name='Примечания (результаты приема)')
    cost = models.IntegerField(verbose_name='Стоимость услуг', default=0)
    summa = models.IntegerField(verbose_name='К оплате', default=0)
    enabled = models.BooleanField(verbose_name='Активен?', default=True)

    def __str__(self):
        return self.mcid.fio

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'