from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from App.forms import Formpost, Uformulario,  UserEditForm, AvatarForm, UserRegisterForm, Msjform
#login
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
def usuarioformulario(request):
        if request.method == "POST":
            form=Uformulario(request.POST)
            print(form)
            if form.is_valid(): 
                info=form.cleaned_data  
                print(info)
                usuario = info.get("usuario")
                email = info.get("email")
                password = info.get("password")
                usuario=User(usuario=usuario,email=email,password=password)              
                usuario.save()
                return render(request, "App/inicio.html",{"mensaje":"Se a registrado con exito"})
            else:
                return(request, "App/uformulario.html",{"mensaje":"Error"})
        else:
            form=Uformulario()
        return render(request, "App/uformulario.html",{"form":form})

def inicio(request):
    return render(request, "App/inicio.html")

def busquedaU(request):
    return render(request, "App/busquedaU.html")

def buscar(request):
    if request.GET["usuario"]:
        us = request.GET["usuario"]
        usuarios = User.objets.filter(usuario=us) 
        if len(usuarios)!=0:
            return render(request, "App/resultadobusqueda.html", {"usuario":usuarios})
        else:
            return render(request,"App/busquedaresultado.html", {"mensaje":"No existe"})
    else:
        return render(request,"App/busquedaresultado.html", {"mensaje":"No existe"})

def leerUsuarios(request):
    usuarios = User.objects.all()
    return render(request,"App/leerusuarios.html", {"usuarios":usuarios})

def eliminaruser(request, id):
    user = User.objects.get(id=id) 
    user.delete()    
    usuarios=User.objects.all()
    return render(request,"App/leerusuarios.html", {"usuario":usuarios} )

def edituser(request,id):
    user = User.objects.get(id=id)
    if request.method=="POST":
        form=Uformulario(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            user.usuario=info["usuario"]
            user.email=info["email"]
            user.password=info["password"]
            user.save()
            usuarios=User.objects.all()
            return render(request,"App/leerusuarios.html", {"usuario":usuarios} )
    else:
        form = Uformulario(initial={"usuario":user.usuario,"email":user.email,"password":user.password})
        return render(request, "App/edituser.html", {"formulario":form, "nameuser":user.usuario, "id":user.id})

def login_u(request):
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usu=request.POST["username"]
            clave=request.POST["password"]
            usuario=authenticate(username=usu,password=clave)
            print(usuario)
            if usuario is not None:
                login(request,usuario)
                return render(request, "App/inicio.html",{"mensaje":f"Bienvenido {usuario}"})
            else:
                return render(request,"App/login.html",{"form":form, "mensaje":"Usuario o contraseña incorrectos"})
        else:
            return render(request,"App/login.html", {"form":form,"mensaje":"FORMULARIO INVALIDO"})
    else:
        form=AuthenticationForm() 
        return render(request, "App/login.html", {"form":form})       

def register(request):
    if request.method=="POST":
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
           
            form.save()
            return render(request, "App/inicio.html",{"mensaje":F"Usuario {username} creado", "imagen":obtenerAvatar(request)})
    else:
        form=UserRegisterForm()
    return render(request, "App/register.html", {"form":form})

def index(request):
    return render(request,"App/index.html")

@login_required 
def editarperfil(request):
    usuario = request.user
    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            
            usuario.first_name=form.cleaned_data["first_name"]
            usuario.last_name=form.cleaned_data["last_name"]
            usuario.email=form.cleaned_data["email"]
            usuario.password1=form.cleaned_data["password1"]
            usuario.password2=form.cleaned_data["password2"]
            usuario.save()
            return render(request, "App/inicio.html", {"mensaje":F"Perfil de {usuario} editado "} )
    else:
        form= UserEditForm(instance=usuario)
        return render(request, "App/editarperfil.html", {"form":form, "usuario":usuario})

@login_required
def agregaravatar(request):
    if request.method == 'POST':
        form=AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatarViejo=Avatar.objects.filter(user=request.user)
            if(len(avatarViejo)>0):
                avatarViejo.delete()
            avatar=Avatar(user=request.user, imagen=form.cleaned_data['imagen'])
            avatar.save()
            return render(request, 'App/agregaravatar', {'usuario':request.user,"formulario":form, 'mensaje':'AVATAR AGREGADO EXITOSAMENTE', "imagen":obtenerAvatar(request)})
    else:
        form=AvatarForm()
    return render(request, 'App/agregaravatar.html', {'formulario':form, 'usuario':request.user, "imagen":obtenerAvatar(request)})

@login_required
def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen=""
    return imagen

@login_required
def borrarAvatar(request):
    avatar=Avatar.objects.filter(user=request.user)
    avatar.delete()
    formavatar=AvatarForm()
    return render(request, "App/agregaravatar.html", {"formavatar":formavatar, "mensajecorrecto":"Avatar eliminado", "imagen":obtenerAvatar(request)})
    # para el blog agregar LoginRequiredMixin

@login_required
def formposteo(request):
    
    if request.method == 'POST':
        form = Formpost(request.POST, request.FILES)

        if form.is_valid():
            info=form.cleaned_data
            autor = request.user.username
            titulo = info["titulo"]
            subtitulo = info["subtitulo"]
            texto = info["texto"]
            img = info["img"]
            fecha = info["fecha"]
            blog = Post(username=autor, titulo=titulo, subtitulo=subtitulo, fecha=fecha, texto=texto, img=img)
            blog.save()
            return render(request, "App/newpost.html", {"mensaje": "Blog creado","imagen":obtenerAvatar(request) })
        else:
            return render(request, "App/newpost.html", {"form":form, "mensaje":"hubo un error en tu solicitud", "imagen":obtenerAvatar(request)})
    else: 
        form = Formpost()
    return render(request,"App/newpost.html",{"form":form, "imagen":obtenerAvatar(request)})
    
@login_required
def borrarBlog(request, id):
    blog=Post.objects.get(id=id)
    blog.delete()
    lista=Post.objects.all()
    return render(request, "App/listablog.html", {"listablog":lista, "mensajecorrecto":"Blog eliminado", "imagen":obtenerAvatar(request)})    

@login_required
def messenger(request):
    if request.method=="POST":
        form=Msjform(request.POST)
        if form.is_valid():
            mensajeform=form.cleaned_data
            emisor=request.user.username
            receptor=mensajeform["receptor"]
            mensaje=mensajeform["mensaje"]
            envio=Msjform(emisor=emisor, receptor=receptor, mensaje=mensaje)
            envio.save()
            return render(request, "App/inicio.html", {"mensaje":"Mensaje enviado", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/mensajes.html", {"form":form, "mensajeerror":"Hubo un error, revisá tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        form=Msjform()
        return render(request, "App/mensajes.html", {"form":form, "imagen":obtenerAvatar(request)})