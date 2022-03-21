from django.contrib import admin
from .models import *
from django import forms


@admin.register(DoctorTypes)
class DoctorTypesAdmin(admin.ModelAdmin):
    """Административное представление модели специализаций"""
    model = DoctorTypes

    list_display = ['name', ]
    list_display_links = ['name', ]
    exclude = ['enabled', ]
    search_fields = ['name', ]

class DoctorsAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DoctorsAdminForm, self).__init__(*args, **kwargs)
        doctors = Doctors.objects.filter().values('schedule')
        schedule_queryset = Schedule.objects.all().exclude(id__in=doctors)
        if self.instance:
            doctors = Doctors.objects.filter(id=self.instance.id).values('schedule')
            active_schedules = Schedule.objects.filter(id__in=doctors)
            schedule_queryset = schedule_queryset | active_schedules
            # schedule_queryset = schedule_queryset.union(active_schedules)
        self.fields['schedule'].queryset = schedule_queryset


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    """Административное представление модели докторов"""
    model = Doctors
    form = DoctorsAdminForm

    list_display = ['get_fullname', 'typeid', 'phone', ]
    list_display_links = ['get_fullname', ]
    exclude = ['enabled', ]
    fields = ['lastname', 'firstname', 'patronymic', 'university', 'experience', 'phone', 'born', 'typeid', 'schedule', 'img', 'image_tag', ]
    readonly_fields = ('image_tag',)
    search_fields = ['lastname', 'firstname', 'patronymic', ]
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

    list_display = ['fio', 'number', 'year', 'policynumber', 'address', 'sign', ]
    exclude = ['enabled', ]

    autocomplete_fields = ['exemptid', ]
    search_fields = ['fio', 'policynumber', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/medcards_masking_fields.js',)




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

    list_display = ['get_patient', 'doctor', 'scheduleid', 'summa', 'close',  ]
    exclude = ['enabled', ]
    autocomplete_fields = ['mcid', 'doctor', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/talons.js',)



