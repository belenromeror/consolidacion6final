from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Vehiculo
from .models import Usuario
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'serial_carroceria', 'serial_motor', 'categoria', 'precio']

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password1')