from django.contrib import admin
from .models import Servicio, Cita
from django.utils.safestring import mark_safe # Necesario para renderizar HTML de la imagen

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    # Añadimos 'mostrar_imagen' a la lista principal
    list_display = ('mostrar_imagen', 'nombre', 'precio', 'duracion_minutos')
    search_fields = ('nombre',)
    
    # Esto permite ver la imagen dentro del formulario de edición
    readonly_fields = ('ver_imagen_grande',)

    def mostrar_imagen(self, obj):
        """Muestra una miniatura en la lista de servicios"""
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />')
        return "Sin imagen"
    
    def ver_imagen_grande(self, obj):
        """Muestra la imagen en grande al editar"""
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="300" style="border-radius: 10px;" />')
        return "No hay imagen cargada"

    mostrar_imagen.short_description = 'Miniatura'
    ver_imagen_grande.short_description = 'Vista previa de imagen'

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora')
    search_fields = ('cliente__username', 'servicio__nombre')
    
    # Esto permite al Admin cambiar el estado rápido desde la lista
    list_editable = ('estado',)