from django import forms
from procesos.models import Proceso
from django.conf import settings

class CrearProcesoFrom(forms.ModelForm):

    class Meta:
        model = Proceso
        fields = ['nombre']

    
        
    