from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def requiere_rol(*roles):
    """
    Decorador para restringir vistas a roles específicos.
    Uso: @requiere_rol("administrador") o @requiere_rol("administrador", "cajero")
    """
    def decorador(vista):
        @wraps(vista)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            try:
                perfil = request.user.perfil
                if perfil.rol not in roles:
                    messages.error(request, "No tienes permiso para acceder a esta sección.")
                    return redirect("dashboard")
            except Exception:
                messages.error(request, "Tu cuenta no tiene perfil asignado.")
                return redirect("login")
            return vista(request, *args, **kwargs)
        return wrapper
    return decorador


def solo_administrador(vista):
    return requiere_rol("administrador")(vista)


def solo_cajero_o_admin(vista):
    return requiere_rol("administrador", "cajero")(vista)
