from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # Importa esto
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from citas.views import (
    registro_cliente, 
    login_cliente, 
    panel_cliente, 
    agendar_cita, 
    catalogo_servicios,
    mis_citas,
    eliminar_cita
)

urlpatterns = [
    # AL PRINCIPIO: La ruta vacía redirige al login
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    
    path('admin/', admin.site.urls),
    path('registro/', registro_cliente, name='registro'),
    path('login/', login_cliente, name='login'),
    path('panel/', panel_cliente, name='panel_cliente'), 
    path('catalogo/', catalogo_servicios, name='catalogo_servicios'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('mis-citas/', mis_citas, name='mis_citas'),
    path('agendar/', agendar_cita, name='agendar_cita'),
    path('eliminar-cita/<int:cita_id>/', eliminar_cita, name='eliminar_cita'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)