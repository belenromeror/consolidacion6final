from django.apps import AppConfig

class VehiculoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vehiculo'

    def ready(self):
        from .models import Usuario
        from django.db.models.signals import post_save

        # Conectar las señales a los receptores
        from .models import asignar_permiso_visualizar_catalogo, asignar_permiso_can_add_vehiculo
        post_save.connect(asignar_permiso_visualizar_catalogo, sender=Usuario)
        post_save.connect(asignar_permiso_can_add_vehiculo, sender=Usuario)
