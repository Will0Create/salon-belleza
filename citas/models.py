from django.db import models
from django.contrib.auth.models import User

class Servicio(models.Model):
    """Los servicios que ofrece el salón (Corte, Tinte, etc.)"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minutos = models.PositiveIntegerField(help_text="Duración en minutos")
    # Nuevo campo para la imagen del servicio
    # Se guardarán en la carpeta /media/servicios/
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Cita(models.Model):
    """La agenda donde se cruzan Clientes y Servicios"""
    ESTADOS = [
        ('P', 'Pendiente'),
        ('C', 'Confirmada'),
        ('X', 'Cancelada'),
        ('F', 'Finalizada'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_citas')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
    fecha_hora = models.DateTimeField()
    notas = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.username} - {self.servicio.nombre} - {self.fecha_hora}"