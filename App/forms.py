from django import forms
from django.contrib.auth.forms import UserCreationForm
from App.models import *
from django.contrib.auth.models import User  
from django.core.exceptions import ValidationError


class Uformulario(forms.Form):
    usuario = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50) 
    password = forms.CharField(max_length=50)

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class UserEditForm(UserCreationForm): 
    email = forms.EmailField(label="Modificar Email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput)
    first_name=forms.CharField(label='Modificar Nombre')
    last_name=forms.CharField(label='Modificar Apellido')
    class Meta:
        model = User
        fields = [ "email", "password1", "password2", 'first_name', 'last_name' ]
        help_text = {k:"" for k in fields}

class AvatarForm(forms.Form):
    imagen= forms.ImageField(label="Imagen")

def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Imagen demasiado grande. El archivo no puede pesar as de  2 MB.') 

class Formpost(forms.Form):
    titulo = forms.CharField(max_length=20, label="Titulo Blog")
    subtitulo = forms.CharField(max_length=50, label="subtitulo")
    texto = forms.CharField(widget=forms.Textarea)
    img = forms.ImageField(label="Adjuntar imagen (opcional)", required=None)
    fecha = forms.DateField(widget=forms.SelectDateWidget, label="Fecha de publicacion * ", initial=date.today)
    
class Msjform(forms.Form):
    usuarios=User.objects.values_list("username","username")
    receptor=forms.ChoiceField(label="Para", widget=forms.Select, choices=usuarios)
    mensaje=forms.CharField(max_length=500, label="Mensaje", widget=forms.Textarea)
