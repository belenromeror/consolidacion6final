from django.shortcuts import render, redirect
from .forms import VehiculoForm
from .models import Vehiculo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth import login
from .forms import RegistroUsuarioForm




def index(request):
    return render(request, 'index.html')
def add_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = VehiculoForm()

    return render(request, 'add_vehiculo.html', {'form': form})


def asignar_permiso_visualizar_catalogo(sender, user, **kwargs):
    permission = Permission.objects.get(codename='visualizar_catalogo')
    user.user_permissions.add(permission)

from django.contrib.auth.signals import user_registered
user_registered.connect(asignar_permiso_visualizar_catalogo)

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asignar el permiso visualizar_catalogo al nuevo usuario
            content_type = ContentType.objects.get_for_model(Vehiculo)
            permission_visualizar, _ = Permission.objects.get_or_create(
                codename='visualizar_catalogo',
                name='Puede visualizar Catálogo de Vehículos',
                content_type=content_type
            )
            user.user_permissions.add(permission_visualizar)

            # Asignar el permiso "Can add vehiculo model" al nuevo usuario
            permission_add, _ = Permission.objects.get_or_create(
                codename='add_vehiculo',
                name='Can add vehiculo model',
                content_type=content_type
            )
            user.user_permissions.add(permission_add)

            # Iniciar sesión automáticamente al registrar un nuevo usuario
            login(request, user)

            return redirect('lista_vehiculos')
        else:
            form = UserCreationForm()

        return render(request, 'registro_usuario.html', {'form': form})


@login_required
def listar(request):
    # Obtener todos los vehículos
    vehiculos = Vehiculo.objects.all()

    # Aplicar las condiciones de precios y agregarlos a la lista de vehículos
    vehiculos_con_condicion = []
    for vehiculo in vehiculos:
        if vehiculo.precio <= 10000:
            vehiculo.condicion_precio = "bajo"
        elif 10000 < vehiculo.precio <= 30000:
            vehiculo.condicion_precio = "medio"
        else:
            vehiculo.condicion_precio = "alto"
        vehiculos_con_condicion.append(vehiculo)

    # Renderizar la lista de vehículos con las condiciones de precios
    return render(request, 'lista_vehiculos.html', {'vehiculos': vehiculos_con_condicion})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Otra página a la que redirigir después del registro exitoso
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_usuario.html', {'form': form})