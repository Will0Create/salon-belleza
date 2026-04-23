from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cita, Servicio
from .forms import CitaForm
from django.contrib.auth.models import User
from django.http import HttpResponse

# --- VISTAS DE AUTENTICACIÓN ---

def registro_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso!")
            return redirect('panel_cliente')
    else:
        form = UserCreationForm()
    return render(request, 'citas/registro.html', {'form': form})

def login_cliente(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Lógica de redirección inteligente:
            if user.is_superuser or user.is_staff:
                return redirect('/admin/') # Administradores al panel de Django
            
            return redirect('panel_cliente') # Clientes a tu panel
    else:
        form = AuthenticationForm()
        # Añadimos clases de Bootstrap para que se vea bien
        form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tu usuario'})
        form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': '********'})
        
    return render(request, 'citas/login.html', {'form': form})

# --- VISTAS DEL PANEL Y NAVEGACIÓN ---

@login_required
def panel_cliente(request):
    # Obtenemos las citas del usuario actual
    citas = Cita.objects.filter(cliente=request.user).order_by('-fecha_hora')
    # Obtenemos todos los servicios para el resumen
    servicios = Servicio.objects.all() 
    
    context = {
        'citas': citas,
        'servicios': servicios,
    }
    return render(request, 'citas/panel.html', context)

@login_required
def catalogo_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'citas/servicios.html', {'servicios': servicios})

@login_required
def mis_citas(request):
    citas = Cita.objects.filter(cliente=request.user).order_by('-fecha_hora')
    return render(request, 'citas/mis_citas.html', {'citas': citas})

# --- ACCIONES DE CITAS ---

@login_required
def agendar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        # Pasamos el usuario al formulario para sus validaciones internas
        form.user = request.user 
        
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = request.user
            cita.estado = 'P'
            cita.save()
            messages.success(request, "¡Cita agendada exitosamente!")
        else:
            # Procesamos errores de validación (como la fecha pasada)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    
    return redirect('panel_cliente')

@login_required
def eliminar_cita(request, cita_id):
    # Buscamos la cita asegurándonos que pertenezca al usuario logueado
    cita = get_object_or_404(Cita, id=cita_id, cliente=request.user)
    
    # Solo permitir eliminar si está pendiente
    if cita.estado == 'P':
        cita.delete()
        messages.success(request, "La cita ha sido cancelada exitosamente.")
    else:
        messages.error(request, "No se puede cancelar una cita que ya ha sido confirmada o finalizada.")
    
    return redirect('mis_citas')
def crear_admin_temporal(request):
    if not User.objects.filter(username='william_admin').exists():
        User.objects.create_superuser('william_admin', 'tu@email.com', 'ClaveDificil123')
        return HttpResponse("Superusuario creado con éxito.")
    return HttpResponse("El usuario ya existe.")