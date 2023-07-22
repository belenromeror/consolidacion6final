from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

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

    @classmethod
    def get_visualizar_catalogo_permission(cls):
        content_type = ContentType.objects.get_for_model(cls)
        permission, _ = Permission.objects.get_or_create(
            codename='visualizar_catalogo',
            name='Puede visualizar Catálogo de Vehículos',
            content_type=content_type,
        )
        return permission

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
