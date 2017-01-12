from django import template
from accounts.models import Usuario
from solicitudes.models import SolicitudVacante
from django.conf import settings

register = template.Library()

@register.filter(name='es_solicitante')
def es_solicitante(user_id, arg):
    return Usuario.objects.filter(
        user__id=user_id, role='SL').exists()

@register.filter(name='es_responsable')
def es_responsable(user_id, arg):
    return Usuario.objects.filter(
        user__id=user_id, role='RP').exists()

@register.filter(name='puede_eliminar_solicitud')
def puede_eliminar_solicitud(user, solicitud):
    usuario = Usuario.objects.filter(user=user, role='RP')
    if solicitud.solicitante == user or usuario.exists():
        return True
    return False

@register.filter(name='null_registro')
def null_registro(value):
    if value != None:
        return value
    else:
        return '----'

@register.filter(name='get_jornada')
def get_jornada(value):
    return [y for x, y in SolicitudVacante.JORNADAS_CHOICES if x  == value][0]

@register.filter(name='get_cargo')
def get_cargo(value):
    return [y for x, y in SolicitudVacante.CARGO_CHOICES if x  == value][0]

@register.filter(name='get_estatus')
def get_estatus(value):
    return [y for x, y in settings.SOLICITUD_ESTATUS_CHOICES if x  == value][0]

@register.filter(name='puede_revisar_y_comentar')
def puede_revisar_y_comentar(user):
    usuario = Usuario.objects.get(user = user)
    if usuario.role == 'RP':
        return 'responsable_del_proceso'
    # if usuario.role == 'JD' or usuario.role == 'A1' or usuario.role == 'A2':
    elif usuario.role != 'SL':
        return 'revisar_y_comentar'
    # elif usuario.role == 'AS':
        # return True#'asignar_responsable'

