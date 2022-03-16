from django.contrib import admin
from .models import *

@admin.register(DoctorTypes)
class DoctorTypesAdmin(admin.ModelAdmin):
    model = DoctorTypes


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    model = Doctors


@admin.register(Exempts)
class ExemptsAdmin(admin.ModelAdmin):
    model = Exempts


@admin.register(Medcards)
class MedcardsAdmin(admin.ModelAdmin):
    model = Medcards


@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    model = Rooms


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    model = Services


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule


@admin.register(Talons)
class TalonsAdmin(admin.ModelAdmin):
    model = Talons



