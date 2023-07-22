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
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    class Meta:
        model = Usuario
        fields = ['username', 'nombre']

    # Agregar campos para los permisos adicionales
    visualizar_catalogo = forms.BooleanField(required=False)
    add_vehiculo = forms.BooleanField(required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        if commit:
            user.save()
            # Asignar los permisos adicionales al usuario
            if self.cleaned_data['visualizar_catalogo']:
                user.user_permissions.add(Vehiculo.get_visualizar_catalogo_permission())
            if self.cleaned_data['add_vehiculo']:
                user.user_permissions.add(Vehiculo.get_add_vehiculo_permission())
        return user

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirigir a la página de inicio después del registro exitoso
    else:
        form = RegistroUsuarioForm()

    return render(request, 'index.html', {'form': form})
