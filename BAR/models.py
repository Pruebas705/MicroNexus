from django.db import models
from django.contrib.auth.models import User


class Sede(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"


class Perfil(models.Model):
    ROL_CHOICES = [
        ("administrador", "Administrador"),
        ("cajero", "Cajero"),
        ("mesero", "Mesero"),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="mesero")
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rol_display()})"

    def es_administrador(self):
        return self.rol == "administrador"

    def es_cajero(self):
        return self.rol == "cajero"

    def es_mesero(self):
        return self.rol == "mesero"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
