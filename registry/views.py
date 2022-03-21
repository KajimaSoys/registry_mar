from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.utils import timezone
import json

def get_medcard(request):
    response = {}
    medcard = request.POST['text']
    medcard = Medcards.objects.get(id=medcard)
    response['isStaff'] = medcard.sign
    try:
        response['exempttype'] = medcard.exemptid.exempttype
        response['exempt'] = medcard.exemptid.exempt
    except Exception:
        response['exempttype'] = ''
        response['exempt'] = 0

    return HttpResponse(json.dumps(response))

def get_schedule(request):
    response = {}
    doctor = request.POST['text']
    url = str(request.POST['link'])
    # print(request.POST['text'])
    doctor = Doctors.objects.get(id=doctor)
    schedule = Schedule.objects.filter(doctors=doctor.id)
    # begin = datetime.datetime.strptime(datetime.datetime.now(), '%H:%M')
    schedule = schedule.filter(free=1).filter(date__gte=datetime.date.today())
    if 'change' in url:
        url = url.replace('http://127.0.0.1:8000/admin/registry/talons/', '').replace('/change/', '')
        talon = Talons.objects.get(id=url)
        schedule_add = Schedule.objects.filter(id=talon.scheduleid_id)
        schedule = schedule | schedule_add
    temp_list = []
    for item in schedule:
        temp_dict = {}
        if item.start > datetime.datetime.now().time():
            temp_dict["schedule_id"] = item.id
            temp_dict["schedule"] = item.__str__()
            temp_list.append(temp_dict)
    response["response"] = temp_list
    # print(response)
    return HttpResponse(json.dumps(response))


def get_record(request):
    response = {}
    record = request.POST['text']
    record = Schedule.objects.get(id=record)
    date = record.date.strftime('%d.%m.%Y')
    start_time = record.start.strftime('%H:%M:%S')

    response["date"] = date
    response["start_time"] = start_time
    print(response)
    return HttpResponse(json.dumps(response))

def get_cost(request):
    services = request.POST['text']
    try:
        import simplejson as json
    except (ImportError,):
        import json
    services = json.loads(services)
    cost = 0
    for item in services:
        cost = cost + Services.objects.get(id=int(item)).cost
    response = {}
    response['cost'] = cost
    return HttpResponse(json.dumps(response))

def change_schedule(request):
    schedule_id = request.POST['text']

    schedule = Schedule.objects.get(id=schedule_id)
    schedule.free = False
    schedule.save()
    response = {}
    response['response'] = 'Operation successful'
    return HttpResponse(json.dumps(response))


