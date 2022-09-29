from django.urls import path
from App.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    
    path("uformulario/", usuarioformulario, name="uformulario"),
    path("inicio/", inicio, name="inicio"),
    path("busquedaU/", busquedaU, name="busquedaU"),
    path("resultadobusqueda/", buscar, name="buscar"),
    path("leerusuarios", leerUsuarios, name="leerUsuarios"),
    path("eliminaruser/<id>", eliminaruser, name="eliminaruser"),
    path("edituser/<id>", edituser, name="edituser"),
    path("login/", login_u , name="login"),
    path("register", register, name="register"),
    path("logout", LogoutView.as_view(template_name="App/logout.html"), name="logout"),
    path("index/", index , name="index"),
    path("editarperfil/", editarperfil, name="editarperfil"),
    path("newpost/", formposteo, name="newpost"),
    path("mensajes/", messenger, name="mensajes"),
    path("agregaravatar/", agregaravatar, name="agregaravatar"),
]
