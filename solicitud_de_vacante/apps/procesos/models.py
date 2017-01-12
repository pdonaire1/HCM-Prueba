from __future__ import unicode_literals
from django.db import models
from solicitudes.models import SolicitudVacante

class Proceso(models.Model):
    nombre = models.CharField('Nombre del proceso',max_length=50, blank=True, null=True)
    solicitud = models.ForeignKey(SolicitudVacante, related_name='solicitud', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

