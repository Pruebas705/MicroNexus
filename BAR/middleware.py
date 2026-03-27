from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


RUTAS_PUBLICAS = ["/", "/login/", "/admin/"]


class PerfilActivoMiddleware:
    """
    Verifica que el usuario autenticado tenga un perfil activo.
    Si el perfil fue desactivado mientras la sesión estaba abierta,
    cierra la sesión automáticamente.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            
            ruta = request.path
            if not any(ruta.startswith(p) for p in ["/admin/", reverse("login")]):
                try:
                    perfil = request.user.perfil
                    if not perfil.activo:
                        from django.contrib.auth import logout
                        logout(request)
                        messages.error(request, "Tu cuenta fue desactivada.")
                        return redirect("login")
                except Exception:
                    pass

        response = self.get_response(request)
        return response
