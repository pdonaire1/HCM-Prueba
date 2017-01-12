from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
# from accounts.models import Usuario

class SolicitudVacante(models.Model):
    NUEVO = 'NV'
    REEMPLAZO = 'RE'
    CARGO_CHOICES = (
        (NUEVO, 'Nuevo'),
        (REEMPLAZO, 'Reemplazo'),
    )
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    JORNADAS_CHOICES = (
        (FULL_TIME, 'Full-time'),
        (PART_TIME, 'Part-time')
    )
    solicitante = models.ForeignKey(User)
    responsable = models.ForeignKey(User, related_name='responsable', blank=True, null=True)
    aprobado_por = models.ForeignKey(User, related_name='aprobado_por', blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    cantidad_vacantes = models.PositiveIntegerField(default=1)
    cargo = models.CharField(
        max_length=2,
        choices=CARGO_CHOICES,
        default=NUEVO,
    )
    jornada = models.CharField(
        max_length=2,
        choices=JORNADAS_CHOICES,
        default=FULL_TIME,
    )
    salario = models.CharField(max_length=50, blank=True, null=True)
    estatus = models.CharField('Enviar a',
        max_length=2,
        choices=settings.SOLICITUD_ESTATUS_CHOICES,
        default=settings.SOLICITUD_ESTATUS_CHOICES[1][0],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    aprobado = models.NullBooleanField(default=None)

class RevisionSolicitud(models.Model):
    usuario = models.ForeignKey(User)
    solicitud = models.ForeignKey(SolicitudVacante)
    aprobado = models.NullBooleanField(default=None, 
        choices=((None, '---'), (True, 'Aprobar'), (False, 'Negar')) )
    comentario = models.CharField(max_length=255, blank=True, null=True)

"""
    Signals
"""
# def create_estatus_solicitud(sender, instance, created, **kwargs):
#     if created:
#         EstatusSolicitud(solicitud=instance, comentario)

# post_save.connect(create_estatus_solicitud, sender=SolicitudVacante)