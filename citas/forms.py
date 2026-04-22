from django import forms
from .models import Cita
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['servicio', 'fecha_hora', 'notas']

    def clean(self):
        cleaned_data = super().clean()
        fecha_hora = cleaned_data.get('fecha_hora')
        servicio = cleaned_data.get('servicio')
        
        # Usamos el usuario que inyectamos desde la vista
        user = getattr(self, 'user', None)

        if fecha_hora and servicio:
            ahora = timezone.now()

            # 1. Validación: No fechas o horas pasadas
            if fecha_hora < ahora:
                raise ValidationError("No puedes agendar una cita en una fecha u hora que ya pasó.")

            # 2. Validación: Solo dentro del mes actual
            if fecha_hora.month != ahora.month or fecha_hora.year != ahora.year:
                raise ValidationError("Solo puedes agendar citas dentro del mes actual.")

            # --- NUEVA LÓGICA: HORARIOS DE OFICINA ---
            hora_elegida = fecha_hora.hour
            dia_semana = fecha_hora.weekday()  # 0=Lunes, 4=Viernes, 5=Sábado, 6=Domingo

            # Lunes a Viernes: 8:00 AM a 9:00 PM (21:00)
            if 0 <= dia_semana <= 4:
                if hora_elegida < 8 or hora_elegida >= 21:
                    raise ValidationError("En días de semana, el horario de atención es de 8:00 AM a 9:00 PM.")
            
            # Sábados y Domingos: 8:00 AM a 2:00 PM (14:00)
            else:
                if hora_elegida < 8 or hora_elegida >= 14:
                    raise ValidationError("Los fines de semana solo atendemos de 8:00 AM a 2:00 PM.")

            # 3. Validación: Choque de horarios (Horario ya ocupado por otro cliente)
            if Cita.objects.filter(fecha_hora=fecha_hora).exclude(estado='X').exists():
                raise ValidationError("Este horario ya está reservado. Por favor elige otro.")

            # 4. Validación: Regla de las 2 semanas por el mismo servicio
            if user:
                rango_inicio = fecha_hora - timedelta(days=14)
                rango_fin = fecha_hora + timedelta(days=14)
                
                # Buscamos si el usuario ya tiene este servicio específico en el rango de tiempo
                cita_existente = Cita.objects.filter(
                    cliente=user, 
                    servicio=servicio, 
                    fecha_hora__range=[rango_inicio, rango_fin]
                ).exclude(estado='X').exists()

                if cita_existente:
                    raise ValidationError(
                        f"Ya tienes una cita para {servicio.nombre} en este periodo. "
                        "Debes esperar al menos 2 semanas para repetir el mismo servicio."
                    )

        return cleaned_data