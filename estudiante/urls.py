from django.urls import path

from . import views

urlpatterns = [
    path('<int:matricula>', views.index, name='index'),
    path('<int:matricula>/practicas/', views.practicas, name='practicas'),
    path('<int:matricula>/horarios/', views.horarios, name='horario')
]