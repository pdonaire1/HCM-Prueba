from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from solicitudes.models import SolicitudVacante, RevisionSolicitud
from accounts.models import Usuario
from procesos.models import Proceso
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from solicitudes.forms import RevisionComentarioSolicitudForm, AsignarResponsableSolicitudForm
from procesos.forms import CrearProcesoFrom
from django.http import HttpResponseRedirect

class CrearSolicitudVacante(CreateView):
    model = SolicitudVacante
    fields = ['descripcion','cantidad_vacantes', 'cargo', 'jornada', 'salario']
    success_url = reverse_lazy('home')
  

    def form_valid(self, form):
        if Usuario.objects.filter(user=self.request.user, role='SL').exists() and form.is_valid():
            form.instance.solicitante = self.request.user
            context = super(CrearSolicitudVacante, self).form_valid(form)
            messages.add_message(self.request, messages.INFO, 'Solicitud agregada satisfactoriamente')
            return context

class ListarSolicitudesVacante(ListView):
    model = SolicitudVacante

    def get_queryset(self):
        usuario = Usuario.objects.get(user=self.request.user)
        if usuario.role == 'SL':
            query = SolicitudVacante.objects.filter(solicitante=self.request.user)
        elif usuario.role == 'RP': # si el usuario es el responsable
            query = SolicitudVacante.objects.filter(estatus=usuario.role, aprobado=True)
        else:  # si el usuario es un aprobador buscamos todas las solicitudes que no
        # han sido revisadas
            query = SolicitudVacante.objects.filter(estatus=usuario.role, aprobado=None)
        return query

class DetailsSolicitudesVacante(DetailView):
    model = SolicitudVacante

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect(url)
        context = self.get_context_data(object=self.object)
        usuario = Usuario.objects.get(user=self.request.user)
        context['comentarios'] = RevisionSolicitud.objects.filter(solicitud=self.object)
        if usuario.role == 'AS':
            form = AsignarResponsableSolicitudForm()
        elif usuario.role == 'RP':
            form = CrearProcesoFrom()
            context['ya_tiene_proceso'] = Proceso.objects.filter(solicitud=self.object).exists()
            proceso = Proceso.objects.filter(solicitud=self.object)
            if proceso.exists():
                context['proceso_id'] = proceso.first().id
        else:
            form = RevisionComentarioSolicitudForm(self.request.user)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        solicitud = context['object']
        usuario = Usuario.objects.get(user=self.request.user)

        # obtenemos el formulario por cada rol de usuario
        if usuario.role == 'AS': # si el usuario es administrador de solicitantes
            form = AsignarResponsableSolicitudForm(request.POST)
        elif usuario.role == 'RP': # si el usuario es el responsable
            form = CrearProcesoFrom(request.POST)
            form.instance.solicitud = solicitud
            if form.save():
                messages.add_message(self.request, messages.INFO, 'Proceso guardado') #set flash
                return HttpResponseRedirect('/listar-solicitud-vacante')
        else:
            form = RevisionComentarioSolicitudForm(self.request.user, request.POST)
        form.request = self.request
        if form.is_valid():
            saved = form.save(self.request.user, solicitud)
            messages.add_message(self.request, messages.INFO, saved[1]) #set flash
            if not saved[0]: # si no fue correctamente guardado lo redireccionamos a la misma vista
                return HttpResponseRedirect('/solicitud-vacante-details/%s'%(solicitud.id))
            return HttpResponseRedirect('/listar-solicitud-vacante')
        messages.add_message(self.request, messages.INFO, 'formulario invalido')
        return HttpResponseRedirect('/solicitud-vacante-details/%s'%(solicitud.id))


class SolicitudVacanteDelete(DeleteView):
    model = SolicitudVacante
    success_url = reverse_lazy('listar-procesos')

    def form_valid(self, form):
        self.object = self.get_object()
        if not self.user_has_permission():
            raise Http404()
        if form.is_valid():
            self.object.delete()
            messages.add_message(self.request, messages.INFO, 'Proceso eliminado') #set flash
            return HttpResponseRedirect(self.get_success_url())
        
        raise Http404()

    def get(self, request, *args, **kwargs):
        if not self.user_has_permission():
            raise Http404()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def user_has_permission(self):
        """
            Si el usuario creo la solicitud o es responsable, puede eliminar
        """
        self.object = self.get_object()
        solicitud = SolicitudVacante.objects.filter(solicitante=self.request.user)
        usuario = Usuario.objects.filter(user=self.request.user, role='RP')
        if usuario.exists() or solicitud.exists():
            return True
        else:
            return False
