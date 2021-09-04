from django.shortcuts import render
from django.http import HttpResponseRedirect
from estudiante.models import Usuario
from .forms import LoginForm
# Create your views here.

def index(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = Usuario.objects.get(username=data["username"])
                if user.pass_field == data["password"]:
                    if user.cargo == "e": # Es estudiante
                        return HttpResponseRedirect('/estudiante/' + user.id)
                    else:
                        return HttpResponseRedirect('/profesor/' + user.id)
                else:
                    context = {
                    "username_form": form["username"],
                    "pass_form": form["password"],
                    "warning_mssg": "Contraseña incorrecta" 
                }
                return render(request, 'login/index.html', context)
            except:
                context = {
                    "username_form": form["username"],
                    "pass_form": form["password"],
                    "warning_mssg": "Usuario no encontrado" 
                }
                return render(request, 'login/index.html', context)
    else:
        form = LoginForm()
    context = {
        "username_form": form["username"],
        "pass_form": form["password"],
        "warning_mssg": ""
    }
    return render(request, 'login/index.html', context)
