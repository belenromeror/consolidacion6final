from django.urls import path
from .views import index, listar, add_vehiculo, iniciar_sesion,cerrar_sesion, registro_usuario, home_page_not_login
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('vehiculo/add/', add_vehiculo, name='add_vehiculo'),
    path('lista_vehiculos/', listar, name='lista_vehiculos'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('registro_usuario/', views.registro_usuario, name='registro_usuario'),
    path('home/', home_page_not_login, name='home'),
]
