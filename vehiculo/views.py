from django.shortcuts import render, redirect
from .forms import VehiculoForm
from .models import Vehiculo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from .forms import RegistroUsuarioForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView



class IndexPageView(TemplateView):
    template_name = 'index.html'

def index(request):
    return render(request, 'index.html')

@permission_required("vehiculo.add_vehiculo", login_url="/login/")
def add_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El vehiculo ha sido creado exitosamente')
            return redirect('listar')
        else:
            messages.error(request, 'Datos incorrectos , favor verificar')
            return HttpResponseRedirect(reverse(add_vehiculo))

    else:
        form = VehiculoForm()
        return render(request, 'add_vehiculo.html', {'form': form})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # No es necesario asignar permisos aquí, las señales se encargarán de eso
            login(request, user)
            return redirect('lista_vehiculos')
    else:
        form = RegistroUsuarioForm()
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


def iniciar_sesion(request):
    if request.method == 'POST':  # si el request es de tipo post
        username = request.POST['username']  # captura username del request
        password = request.POST['password']  # captura password del request
        user = authenticate(request, username=username, password=password)  # se captura el usuario encontrado
        if user is not None:  # si el usuario autenticado no viene vacio, quiere decir es validas sus credenciales
            login(request, user)
            return redirect('lista_vehiculos')
        else:
            messages.error(request, 'Usuario o password inválidas')
            return render(request, 'login.html')
    return render(request, 'login.html')  # tipo get


# view o controlador para cerrar sesion
@login_required
def cerrar_sesion(request):
    logout(request)  # se deslogue
    return render(request, 'login.html')


def home_page_not_login(request):
    return render(request, 'index.html')
