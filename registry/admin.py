from django.contrib import admin
from .models import *
from django import forms
from django.urls import re_path as url
from django.utils.html import format_html
from django.urls import reverse
from . import data_format, waybill_engine
from django.http import HttpResponse, HttpResponseRedirect
from slugify import slugify
import os

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
    fields = ['lastname', 'firstname', 'patronymic', 'university', 'experience', 'phone', 'born', 'typeid', 'schedule', 'img', 'image_tag', 'created_by', ]
    readonly_fields = ('image_tag',)
    search_fields = ['lastname', 'firstname', 'patronymic', ]
    autocomplete_fields = ['typeid', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/doctor_masking.js',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if request.user.groups.filter(name='doctors').exists():
            readonly_fields = ('img', 'image_tag', 'created_by', )
        else:
            readonly_fields = ('image_tag', )
        return readonly_fields

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='doctors').exists():
            doctor = Doctors.objects.filter(created_by=request.user.id)[0]
            talons = Talons.objects.filter(doctor_id=doctor.id).values('mcid')
            # medcards = Medcards.objects.filter(id__in=talons)
            # return medcards
            return qs.filter(id__in=talons)
        else:
            return qs


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

    list_display = ['get_patient', 'doctor', 'scheduleid', 'summa', 'close', 'talon_actions', ]
    exclude = ['enabled', ]
    autocomplete_fields = ['mcid', 'doctor', ]
    search_fields = ['mcid__fio', 'doctor__lastname', 'scheduleid__date', 'scheduleid__start', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/talons.js',)

    def get_urls(self):
        urls = super(TalonsAdmin, self).get_urls()
        custom_urls = [
            url(
                r'^(?P<id>.+)/save_check/$',
                self.admin_site.admin_view(self.save_check),
                name='save_check',
            ),
        ]
        return custom_urls + urls

    def talon_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">&nbsp  Акт оказанных услуг &nbsp</a>'
            '<p></p>',
            reverse('admin:save_check', args=[obj.pk]),
        )
    talon_actions.short_description = 'Выписка'
    talon_actions.allow_tags = True

    def save_check(self, request, id,  *args, **kwargs):
        data = data_format.get_order_data(int(id))
        path = waybill_engine.waybill_generate(data)
        temp = slugify(path.split('/')[2], save_order=True, separator='.')
        if os.path.exists(path):
            with open(path, 'rb') as fh:
                response = HttpResponse(fh.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'inline; filename=' + temp
                return response

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='doctors').exists():
            doctor = Doctors.objects.filter(created_by=request.user.id)[0]
            return qs.filter(doctor_id=doctor.id)
        else:
            return qs

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if request.user.groups.filter(name='doctors').exists():
            readonly_fields = ('mcid', 'doctor', 'scheduleid', 'datestart', 'timestart', 'service', 'cost', 'summa', )
        return readonly_fields
