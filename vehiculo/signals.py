from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Obtener el modelo de usuario personalizado
User = get_user_model()
# Definir una función para asignar el permiso visualizar_catalogo
@receiver(post_save, sender=User)
def asignar_permiso_visualizar_catalogo(instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(Vehiculo)
        permission, _ = Permission.objects.get_or_create(
            codename='visualizar_catalogo',
            name='Puede visualizar Catálogo de Vehículos',
            content_type=content_type
        )
        instance.user_permissions.add(permission)