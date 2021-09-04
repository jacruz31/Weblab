from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from estudiante.models import Usuario, Registro, Horario
from estudiante.views import get_weekday
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
    return render(request, 'profesor/index.html', context)

def registrar(request, matricula):
    # Estudiantes que no tengan un registro
    estudiantes_disponibles = Usuario.objects.filter(cargo="e").exclude(registro__in=Registro.objects.all())
    horarios_disponibles = Horario.objects.filter(disponible=True).select_related('laboratorio')
    context = {
        "estudiantes": estudiantes_disponibles,
        "matricula": matricula,
    }
    if request.method == "POST":
        if "register_estudiante" in request.POST:
            return HttpResponseRedirect(request.path + request.POST["register_estudiante"])
    storage = get_messages(request)
    for message in storage:
        print(message)
    return render(request, 'profesor/registrar.html', context)

def registrar_horario(request, matricula, estudiante):
    # En la funcion registrar, poner un redirect con la matricula del estudiante a registrar
    # En registrar_horario, mostrar los horarios disponibles y hacer efectivo el registro

    # Estudiante escogido
    estudiante_chosen = Usuario.objects.get(pk=estudiante)
    # Horarios disponibles
    horarios_disponibles = Horario.objects.filter(disponible=True).select_related('laboratorio')
    context = {
        "matricula": matricula,
        "estudiante_chosen": estudiante_chosen,
        "horarios": horarios_disponibles,
    }
    if request.method == "POST":
        if "register" in request.POST:
            horario_chosen = Horario.objects.get(pk=request.POST["register"])
            registro_creado = Registro(estudiante=estudiante_chosen, horario=horario_chosen)
            registro_creado.save()
            horario_chosen.disponible = False
            horario_chosen.save()
            messages.success(request, "Se ha registrado el estudiante %s %s (%s) en el horario de %s, %s a %s de la materia %s (Paralelo %d) con el profesor %s %s"%(estudiante_chosen.nombres, estudiante_chosen.apellidos, estudiante_chosen.id, get_weekday(horario_chosen.fecha.weekday()), horario_chosen.hora_inicio, horario_chosen.hora_fin, horario_chosen.laboratorio.materia, horario_chosen.laboratorio.paralelo, horario_chosen.laboratorio.profesor.nombres, horario_chosen.laboratorio.profesor.apellidos))
            return HttpResponseRedirect("/profesor/" + str(matricula) + "/registrar/")
    return render(request, 'profesor/registrarhorario.html', context)

