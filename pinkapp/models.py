from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Usuario(User):
    class Meta:
        proxy = True

GENERO = (
		('M','Ellos'),
		('F','Ellas'),
		('N','Ninguno'),
		)

class marca(models.Model):
	nombre = models.CharField(max_length = 120)
	imagen = models.ImageField(upload_to = 'static/uploads/')
	generoPrincipal = models.CharField(max_length = 1, choices=GENERO)
	generoSecundario = models.CharField(max_length = 1, choices=GENERO)

	class Meta:
		verbose_name = 'Marca'
		verbose_name_plural ="Marcas"

	def __unicode__(self):
		return self.nombre


class perfume(models.Model):
	nombre = models.CharField(max_length= 120)
	marca = models.ForeignKey(marca)
	precio = models.FloatField()
	presentacion = models.CharField(max_length= 120)
	generoPrincipal = models.CharField(max_length= 1, choices=GENERO)
	generoSecundario = models.CharField(max_length= 1, choices=GENERO)
	imagen = models.ImageField(upload_to = 'static/uploads/')

	class Meta:
		verbose_name = 'Perfume'
		verbose_name_plural ="Perfumes"

	def __unicode__(self):
		return self.nombre

