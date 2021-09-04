from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.utils import timezone

import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_weekday(index):
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return days[index]

from .models import Usuario, Horario, Registro, Laboratorio

# Create your views here.
def index(request, matricula):
    try:
        user_estudiante = Usuario.objects.get(pk=matricula)
        cargo = "Estudiante" if user_estudiante.cargo == "e" else "Profesor"
        context = {
            'user_estudiante': user_estudiante,
            'cargo': cargo,
            'isFound': True
        }
    except:
        context = {
            'user_estudiante': "",
            'cargo': "",
            'isFound': False
        }
    return render(request, 'estudiante/index.html', context)


def practicas(request, matricula):
    try:
        registro_estudiante = Registro.objects.get(estudiante=matricula)
        now = datetime.datetime.now()
        now_time = now.time()
        fecha = registro_estudiante.horario.fecha
        hora_inicio = registro_estudiante.horario.hora_inicio
        hora_fin = registro_estudiante.horario.hora_fin
        local_ip = get_ip_address()
        # print(now, now.strftime("%A"), now.weekday())
        # print(fecha, fecha.strftime("%A"), fecha.weekday())
        port = "5000"
        context = {
            'matricula' : matricula,
            'ipv4': local_ip,
            'port': port,
            'horario': registro_estudiante.horario,
            'day': get_weekday(fecha.weekday()),
            'isInDay': fecha.weekday() == now.weekday(),
            'isRegisterFound': True,
            'isInTime': now_time >= hora_inicio and now_time <= hora_fin
        }
    except Exception as e:
        print(e)
        context = {
            'matricula' : matricula,
            'ipv4': "",
            'port': "",
            'laboratorio': "",
            'horario': "",
            'isRegisterFound': False,
            'isInTime': False
        }
    return render(request, 'estudiante/practica.html', context)

def horarios(request, matricula):
    horarios_disponibles = Horario.objects.filter(disponible=True).select_related('laboratorio')
    registro_estudiante = Registro.objects.filter(estudiante=matricula)
    context = {
        'matricula' : matricula,
        'horarios_disponibles': horarios_disponibles,
        'registros': registro_estudiante,
    }
    if request.method == "POST":
        if "register" in request.POST:
            if len(registro_estudiante) == 0:
                lista_registro = request.POST["register"].split("#")
                estudiante_registered = Usuario.objects.get(pk=lista_registro[0])
                horario_registered = Horario.objects.get(pk=lista_registro[1])
                registro_creado = Registro(estudiante=estudiante_registered, horario=horario_registered)
                registro_creado.save()
                context['registros'] = [registro_creado]
                horario_registered.disponible = False
                horario_registered.save()
                registro_estudiante = registro_creado
        if "delete_register" in request.POST:
            to_delete_register_id = request.POST["delete_register"]
            to_delete_register = Registro.objects.get(pk=to_delete_register_id)
            horario_registered = to_delete_register.horario
            horario_registered.disponible = True
            horario_registered.save()
            to_delete_register.delete()
    return render(request, 'estudiante/horario.html', context)
