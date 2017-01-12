from django import forms
from solicitudes.models import RevisionSolicitud
from django.conf import settings
from accounts.models import Usuario
from django.contrib import messages
from django.contrib.auth.models import User

class RevisionComentarioSolicitudForm(forms.ModelForm):

    class Meta:
        model = RevisionSolicitud
        fields = ['aprobado', 'comentario']
    
    def __init__(self, aprobador,*args, **kwargs):
        super(RevisionComentarioSolicitudForm, self).__init__(*args, **kwargs)
        usuario = Usuario.objects.get(user=aprobador)
        # retornamos las opciones para cada tipo de usuario:
        ENVIAR_A_CHOICES = self.return_enviar_a_choices(usuario.role)
        self.fields['enviar_a'] = forms.CharField(
            max_length=2,
            widget=forms.Select(choices=ENVIAR_A_CHOICES),
        )
        self.Meta.fields.append('enviar_a')
        
    def return_enviar_a_choices(self, role):
        """
            Este metodo retorna el listado de opciones que tiene cada 
            tipo de usuario dependiendo del rol
        """
        ENVIAR_A_CHOICES = list(settings.SOLICITUD_ESTATUS_CHOICES)
        while role != ENVIAR_A_CHOICES[0][0]:
            del ENVIAR_A_CHOICES[0]
        del ENVIAR_A_CHOICES[0]
        del ENVIAR_A_CHOICES[-1]
        return tuple([('-', '---')] + ENVIAR_A_CHOICES)

    def save(self, aprobador, solicitud):
        enviar_a = self.cleaned_data.get("enviar_a")
        revision = RevisionSolicitud(
            usuario=aprobador,
            solicitud=solicitud,
            aprobado=self.cleaned_data.get("aprobado"),
            comentario=self.cleaned_data.get("comentario"))
        # validamos el formulario
        if revision.aprobado == None:
            return (False, 'El campo aprobado es obligatoria')
        if revision.aprobado and enviar_a == '-':
            return (False, 'El campo "enviar a" es obligatoria, la solicitud es aprobada')
        if (not revision.aprobado) and self.cleaned_data.get("comentario") == '':
            if enviar_a != '-':
                messages.add_message(self.request, messages.INFO, 'Si es negada la solicitud, no sera enviada para su revision por otra persona')
            return (False, 'El Comentario es obligatorio')

        revision.save()
        if revision.aprobado:
            solicitud.estatus = enviar_a
        else:
            solicitud.aprobado=False
            solicitud.estatus = 'SL'
        solicitud.save()
        return (True, 'Guardado')

class AsignarResponsableSolicitudForm(forms.Form):
    responsable = forms.ChoiceField(label="Asignar responsable", choices = [])
    
    def __init__(self, *args, **kwargs):
        super(AsignarResponsableSolicitudForm, self).__init__(*args, **kwargs)
        self.fields['responsable'].choices = [(x.pk, x.username) for x in User.objects.all()]

    def save(self, user, solicitud):
        responsable = User.objects.get(id=self.cleaned_data['responsable'])
        solicitud.estatus = 'RP'
        solicitud.aprobado_por = user
        solicitud.responsable = responsable
        solicitud.aprobado = True
        solicitud.save()
        return (True, 'Cambios guardados')
