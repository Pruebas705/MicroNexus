from django.contrib import admin
from .models import Sede, Perfil


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "activa", "creada_en")
    list_filter = ("activa",)
    search_fields = ("nombre",)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "rol", "sede", "activo")
    list_filter = ("rol", "sede", "activo")
    search_fields = ("usuario__username", "usuario__email")
