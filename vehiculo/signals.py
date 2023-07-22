from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Vehiculo

@receiver(post_migrate, sender=AppConfig)
def create_permissions(sender, **kwargs):
    # Verificar si los permisos ya han sido creados
    if not Permission.objects.filter(codename='visualizar_catalogo').exists():
        content_type = ContentType.objects.get_for_model(Vehiculo)
        Permission.objects.create(
            codename='visualizar_catalogo',
            name='Puede visualizar Catálogo de Vehículos',
            content_type=content_type,
        )

    if not Permission.objects.filter(codename='add_vehiculo').exists():
        content_type = ContentType.objects.get_for_model(Vehiculo)
        Permission.objects.create(
            codename='add_vehiculo',
            name='Can add vehiculo model',
            content_type=content_type,
        )
