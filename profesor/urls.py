from django.urls import path

from . import views

urlpatterns = [
    path('<int:matricula>', views.index, name='index'),
    path('<int:matricula>/registrar/', views.registrar, name='registrar'),
    path('<int:matricula>/registrar/<int:estudiante>', views.registrar_horario, name='registrar_horario')
]