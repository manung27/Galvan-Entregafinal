from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from datetime import date, datetime
# Create your models here.

class User(models.Model): 
    usuario = models.CharField(max_length=50)
    email = models.EmailField(max_length=50) 
    password = models.CharField(max_length=50) 
    
    def __str__(self): #para que aparezca el nombre en el admin django y no como me aparecia antes 
        return self.usuario+""

class Avatar(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    imagen= models.ImageField(upload_to='avatares', null=True, blank=True)

class Post(models.Model):

    titulo = models.CharField(max_length=270)
    subtitulo = models.CharField(max_length=200)
    texto = models.TextField(max_length=2700)
    username = models.CharField(max_length=50)
    img = models.ImageField(upload_to='blogs', null=True, blank=True)
    fecha = models.DateField(default=datetime.now)
    def __str__(self) -> str:
        return str(self.username)+", "+self.titulo

class Messenger(models.Model):
    emisor=models.CharField(max_length=50, null=True)
    receptor=models.CharField(max_length=50, null=True)
    mensaje=models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return "De: "+str(self.emisor)+", Para: "+str(self.receptor)







