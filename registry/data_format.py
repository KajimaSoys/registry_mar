from . import models
from django.db.models.functions import datetime
from datetime import datetime, timedelta
from num2words import num2words


def get_order_data(id):
    talon = models.Talons.objects.filter(id=id).values()[0]
    patient = models.Medcards.objects.filter(id=talon['mcid_id']).values()[0]
    services = models.Services.objects.filter(talons=id).values()
    doctor = models.Doctors.objects.filter(id=talon['doctor_id']).values()[0]

    obj = obj_container(talon, patient, services, doctor)
    print(obj)
    return obj

def obj_container(talon, patient, services, doctor):
    obj = []

    service_list = []
    for item in services:
        item.pop('id', None)
        item.pop('enabled', None)
        service_list.append(item)

    # obj.extend([placement, patient, service_list])
    obj.extend([talon, patient, service_list, doctor])
    return obj

def format(data):
    dict = {}

    talon = data[0]
    dict['id'] = talon['id']
    dict['date_start'] = datetime.strftime(talon['datestart'], "%d.%m.%Y")
    dict['time_start'] = talon['timestart'].strftime("%H:%M") #datetime.strftime(talon['timestart'], "%H:%M")
    dict['date_start_word'] = date2word(dict['date_start'])
    dict['summa'] = talon['summa']

    patient = data[1]
    patient_name = patient['fio']
    dict['patient_name'] = patient_name
    temp = patient_name.split(' ')
    dict['patient_name_output'] = temp[0] + ' ' + temp[1][:1] + '.' + temp[2][:1] + '.'
    dict['address'] = patient['address']
    dict['number'] = patient['number']
    dict['born'] = datetime.strftime(patient['year'], "%d.%m.%Y")
    dict['year_word'] = date2word(dict['born'])
    dict['path'] = f'{temp[0]}{temp[1][:1]}.{temp[2][:1]}_{dict["id"]}'

    service = data[2]
    service_name = []
    cost = []
    for item in service:
        service_name.append(item['name'])
        cost.append(item['cost'])
    dict['service_name'] = service_name
    dict['cost'] = cost

    doctor = data[3]
    dict['doctor_name'] = f"{doctor['lastname']} {doctor['firstname']} {doctor['patronymic']}"

    return dict


def date2word(date):
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_list = date.split('.')
    date_list[1] = month_list[int(date_list[1]) - 1]
    return date_list


def n2w(num):
    return num2words(num, lang='ru')