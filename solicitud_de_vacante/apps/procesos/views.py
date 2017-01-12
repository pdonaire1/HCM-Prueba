from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView
from django.views.generic import DetailView
from procesos.models import Proceso
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from solicitudes.models import SolicitudVacante
from accounts.models import Usuario

class ProcesoDetails(DetailView):
    model = Proceso
    fields = ['nombre','cantidad_vacantes', 'cargo', 'jornada', 'salario']
    success_url = reverse_lazy('home')
  

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except:
            return redirect('home')
        context = self.get_context_data(object=self.object)
        
        return self.render_to_response(context)

class ListarProcesos(ListView):
    model = Proceso

    def get_queryset(self):
        return Proceso.objects.filter(solicitud__responsable=self.request.user)

class ProcesoDelete(DeleteView):
    model = Proceso
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
        self.object = self.get_object()
        solicitud = SolicitudVacante.objects.filter(solicitante=self.request.user)
        usuario = Usuario.objects.filter(user=self.request.user, role='RP')
        if usuario.exists() or solicitud.exists():
            return True
        else:
            return False
