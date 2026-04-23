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
            
            # Redirección inteligente
            if user.is_superuser or user.is_staff:
                return redirect('/admin/') 
            
            return redirect('panel_cliente')
    else:
        form = AuthenticationForm()
        # Clases de Bootstrap para los inputs
        form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tu usuario'})
        form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': '********'})
        
    return render(request, 'citas/login.html', {'form': form})

# --- VISTAS DEL PANEL Y NAVEGACIÓN ---

@login_required
def panel_cliente(request):
    citas = Cita.objects.filter(cliente=request.user).order_by('-fecha_hora')
    servicios = Servicio.objects.all() 
    return render(request, 'citas/panel.html', {'citas': citas, 'servicios': servicios})

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
        form.user = request.user 
        
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = request.user
            cita.estado = 'P'
            cita.save()
            messages.success(request, "¡Cita agendada exitosamente!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    
    return redirect('panel_cliente')

@login_required
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, cliente=request.user)
    if cita.estado == 'P':
        cita.delete()
        messages.success(request, "La cita ha sido cancelada exitosamente.")
    else:
        messages.error(request, "No se puede cancelar una cita confirmada.")
    return redirect('mis_citas')

# --- FUNCIÓN DE EMERGENCIA PARA SUPERUSER ---

def crear_admin_temporal(request):
    # Usamos 'get_or_create' para que no falle si ya existe
    user, created = User.objects.get_or_create(username='william_admin')
    
    # Forzamos la contraseña y los permisos de jefe
    user.set_password('Salon2026!') 
    user.is_superuser = True
    user.is_staff = True
    user.save()
    
    if created:
        return HttpResponse("¡Superusuario 'william_admin' creado exitosamente!")
    else:
        return HttpResponse("¡La contraseña de 'william_admin' ha sido actualizada a 'Salon2026!'!")