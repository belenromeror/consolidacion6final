from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Vehiculo
from .models import Usuario
from django.shortcuts import render

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'serial_carroceria', 'serial_motor', 'categoria', 'precio']

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password1')


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirigir a la página de inicio después del registro exitoso
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_usuario.html', {'form': form})
