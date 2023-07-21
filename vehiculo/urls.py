from django.urls import path
from .views import index, add_vehiculo, listar

urlpatterns = [
    path('', index, name='index'),
    path('vehiculo/add/', add_vehiculo, name='add_vehiculo'),
    path('lista_vehiculos/', listar, name='lista_vehiculos'),
]
