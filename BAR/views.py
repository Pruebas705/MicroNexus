from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil


def vista_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            try:
                perfil = user.perfil
                if not perfil.activo:
                    messages.error(request, "Tu cuenta está desactivada. Contacta al administrador.")
                    return render(request, "BAR/login.html")
            except Perfil.DoesNotExist:
                messages.error(request, "Tu cuenta no tiene un perfil asignado.")
                return render(request, "BAR/login.html")

            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "BAR/login.html")


def vista_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        logout(request)
        messages.error(request, "Tu cuenta no tiene perfil. Contacta al administrador.")
        return redirect("login")

    contexto = {
        "perfil": perfil,
        "usuario": request.user,
    }
    return render(request, "BAR/dashboard.html", contexto)
