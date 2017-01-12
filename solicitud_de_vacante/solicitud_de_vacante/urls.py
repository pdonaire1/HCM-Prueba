"""solicitud_de_vacante URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from solicitudes import views as solicitudes_views
from procesos import views as procesos_views
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    # Solicitudes
    url(r'^crear-solicitud-vacante$', solicitudes_views.CrearSolicitudVacante.as_view(), 
        name='crear-solicitud-vacante'),
    url(r'^listar-solicitud-vacante$', solicitudes_views.ListarSolicitudesVacante.as_view(), 
        name='listar-solicitud-vacante'),
    url(r'^solicitud-vacante-details/(?P<pk>[0-9]+)$', solicitudes_views.DetailsSolicitudesVacante.as_view(), 
        name='solicitud-vacante-details'),
    url(r'^eliminar-solicitud/(?P<pk>[0-9]+)$', solicitudes_views.SolicitudVacanteDelete.as_view(), 
        name='eliminar-solicitud'),

    # Procesos
    url(r'^proceso-details/(?P<pk>[0-9]+)$', procesos_views.ProcesoDetails.as_view(), 
        name='proceso-details'),
    url(r'^listar-procesos$', procesos_views.ListarProcesos.as_view(), 
        name='listar-procesos'),
    url(r'^eliminar-proceso/(?P<pk>[0-9]+)$', procesos_views.ProcesoDelete.as_view(), 
        name='eliminar-proceso'),
    

]
