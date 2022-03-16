from django.contrib import admin
from .models import *

@admin.register(DoctorTypes)
class DoctorTypesAdmin(admin.ModelAdmin):
    """Административное представление модели специализаций"""
    model = DoctorTypes

    list_display = ['name', ]
    list_display_links = ['name', ]
    exclude = ['enabled', ]
    search_fields = ['name', ]


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    """Административное представление модели докторов"""
    model = Doctors

    list_display = ['get_fullname', 'typeid', 'phone', ]
    list_display_links = ['get_fullname', ]
    exclude = ['enabled', ]
    search_fields = ['get_fullname']
    autocomplete_fields = ['typeid', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/doctor_masking.js',)


@admin.register(Exempts)
class ExemptsAdmin(admin.ModelAdmin):
    """Административное представление модели льгот"""
    model = Exempts

    list_display = ['exempttype', 'exempt', ]
    exclude = ['enabled', ]
    search_fields = ['exempttype', ]


@admin.register(Medcards)
class MedcardsAdmin(admin.ModelAdmin):
    model = Medcards

'medcards_masking_fields.js'


@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    """Административное представление модели кабинетов"""
    model = Rooms

    list_display = ['number', ]
    exclude = ['enabled', ]
    search_fields = ['number', ]


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    """Административное представление модели услуг"""
    model = Services

    list_display = ['name', 'cost', ]
    exclude = ['enabled', ]
    search_fields = ['name', ]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Административное представление модели расписаний"""
    model = Schedule

    list_display = ['__str__', 'roomid', 'free', ]
    ordering = ['date']
    exclude = ['enabled', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/schedule_masking.js',)


@admin.register(Talons)
class TalonsAdmin(admin.ModelAdmin):
    model = Talons



