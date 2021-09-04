# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Horario(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    laboratorio = models.ForeignKey('Laboratorio', models.DO_NOTHING, db_column='laboratorio', blank=True, null=True)
    disponible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horario'


class Laboratorio(models.Model):
    materia = models.CharField(max_length=50)
    paralelo = models.IntegerField()
    profesor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='profesor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'laboratorio'


class Registro(models.Model):
    horario = models.ForeignKey(Horario, models.DO_NOTHING, db_column='horario', blank=True, null=True)
    estudiante = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='estudiante', blank=True, null=True)

    def __str__(self):
        return str(self.horario.id) + ", " + str(self.estudiante.id)
    
    class Meta:
        managed = False
        db_table = 'registro'


class Usuario(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    pass_field = models.CharField(db_column='pass', max_length=50)  # Field renamed because it was a Python reserved word.
    email = models.CharField(max_length=100)
    cargo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
