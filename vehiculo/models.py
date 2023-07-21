from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .signals import asignar_permiso_visualizar_catalogo
from django.utils.translation import gettext_lazy as _


class Vehiculo(models.Model):
    MARCA_CHOICES = [
        ('Fiat', 'Fiat'),
        ('Chevrolet', 'Chevrolet'),
        ('Ford', 'Ford'),
        ('Toyota', 'Toyota'),
    ]

    CATEGORIA_CHOICES = [
        ('Particular', 'Particular'),
        ('Transporte', 'Transporte'),
        ('Carga', 'Carga'),
    ]

    marca = models.CharField(max_length=20, choices=MARCA_CHOICES, default='Ford')
    modelo = models.CharField(max_length=100)
    serial_carroceria = models.CharField(max_length=50)
    serial_motor = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='Particular')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.marca} - {self.modelo}"


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=15, blank=True, null=True)
    contraseña = models.CharField(max_length=100, blank=True, null=True)

    # Agregar related_name para evitar conflictos con User.groups
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="usuarios",  # Cambiar "usuarios" por un nombre único
        related_query_name="usuario",
    )

    # Agregar related_name para evitar conflictos con User.user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="usuarios_permissions",  # Cambiar "usuarios_permissions" por un nombre único
        related_query_name="usuario",
    )

    def __str__(self):
        return self.username

def asignar_permiso_visualizar_catalogo(instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(Vehiculo)
        permission, _ = Permission.objects.get_or_create(
            codename='visualizar_catalogo',
            name='Puede visualizar Catálogo de Vehículos',
            content_type=content_type
        )
        instance.user_permissions.add(permission)


@receiver(post_save, sender=Usuario)
def on_usuario_post_save(sender, instance, created, **kwargs):
    asignar_permiso_visualizar_catalogo(sender, instance, created, **kwargs)


def asignar_permiso_can_add_vehiculo(instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(Vehiculo)
        permission, _ = Permission.objects.get_or_create(
            codename='add_vehiculo',
            name='Can add vehiculo model',
            content_type=content_type
        )
        instance.user_permissions.add(permission)
