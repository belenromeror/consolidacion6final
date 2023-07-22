# proyecto_vehiculos_django/vehiculo/admin.py

from django.contrib import admin
from .models import Vehiculo

class VehiculoAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    list_display = ('marca', 'modelo', 'serial_carroceria', 'serial_motor', 'precio')
    list_filter = ('marca', 'modelo', 'serial_carroceria', 'serial_motor', 'precio')

admin.site.register(Vehiculo)