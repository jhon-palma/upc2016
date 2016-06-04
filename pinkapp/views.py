# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.template import RequestContext
from .models import marca, perfume
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from validators import FormContacto,FormLoginValidator,FormRegistroValidator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from .models import Usuario

def index(request):
	return render_to_response('index.html')

def marcas(request):
	marcas = marca.objects.all()
	return render_to_response('marcas.html',{'marcas': marcas}, context_instance = RequestContext(request))

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
def search(request):
    """view de los resultados de busqueda
    """
    lista = None
    filter = None
    if 'filter' in request.GET.keys():
        filter = request.GET['filter']
        
        detalle = False
        if  'marca' in request.GET:
        	qset = ( ( Q( generoPrincipal = filter) |
                Q( generoSecundario = filter)) &
                Q(marca_id = request.GET['marca'])
                )
        	listado = perfume.objects.filter(qset)
        	detalle = True
        	
        else:
        	qset = ( Q( generoPrincipal = filter) |
                Q( generoSecundario = filter)
                )
        	listado = marca.objects.filter(qset)

        paginador = Paginator( listado, 16)
        page = 1
        if 'page' in request.GET:
            page = request.GET['page']
        try:
            lista = paginador.page(page)
        except EmptyPage:
            lista = paginador.page( paginador.num_pages)
        except PageNotAnInteger:
            raise Http404("Pagina no encontrada")

    return render_to_response('search.html', {'lista': lista, 'detalle': detalle, 'paginador': paginador, 'filtro': filter  }, context_instance = RequestContext(request))

#import pdb;     
def contacto(request):
 #   pdb.set_trace()
    if request.method == 'POST':
        validator = FormContacto(request.POST)
        validator.required = ['name', 'email', 'telefono', 'asunto', 'mensaje']

        if validator.is_valid():
            htmly = get_template('mail.html')

            name = request.POST['name']
            from_email = request.POST['email']
            telefono = request.POST['telefono']
            asunto = request.POST['asunto']
            ast = "Dudas o inquietud Perfumes Pink/826"
            mensaje = request.POST['mensaje']
            body = render_to_string('mail.html',{'name':name,'asunto':asunto,'from_email':from_email,'telefono':telefono, 'mensaje':mensaje})
            #contexto = Context({name})
            #html_content = htmly.render(contexto)

            msg = EmailMultiAlternatives(ast, body , from_email ,  [ settings.EMAIL_HOST_USER])
            #msg.attach_alternative(html_content, "text/html")
            #msg.send()
            msg.content_subtype = "html"
            msg.send()

            #send_mail(asunto, body, from_email ,  [ settings.EMAIL_HOST_USER] )
            return render_to_response('contacto.html', {'success': True, 'error':validator.getMessage()}, context_instance = RequestContext(request))
        else:
            return render_to_response('contacto.html', {'error': validator.getMessage()}, context_instance=RequestContext(request))
    return render_to_response('contacto.html',  context_instance=RequestContext(request))


def comprar(request):

    filter = request.GET['filter']

    producto=perfume.objects.get(id=filter)

    if request.method == 'POST':
        validator = FormContacto(request.POST)
        validator.required = ['name', 'email', 'telefono', 'direccion']
        if validator.is_valid():
            htmly = get_template('mailCompra.html')

            name = request.POST['name']
            from_email = request.POST['email']
            telefono = request.POST['telefono']
            producto = request.POST['producto']
            ast = "Venta Perfumes Pink/826"
            precio = request.POST['precio']
            body = render_to_string('mailCompra.html',{'name':name,'producto':producto,'direccion':direccion, 'from_email':from_email,'telefono':telefono, 'precio':precio})
            
            msg = EmailMultiAlternatives(ast, body , from_email ,  [ settings.EMAIL_HOST_USER])
            msg.content_subtype = "html"
            msg.send()

            return render_to_response('compraExitosa.html', {'success': True, 'error':validator.getMessage()}, context_instance = RequestContext(request))
        else:
            return render_to_response('comprar.html', {'error': validator.getMessage()}, context_instance=RequestContext(request))

    return render_to_response('comprar.html', {'producto':producto, 'filtro': filter}, context_instance = RequestContext(request))

import xhtml2pdf.pisa as pisa
from StringIO import StringIO
from django.template.loader import render_to_string

def verpdf(request):
    result = StringIO() #creamos una instancia del un objeto StringIO para    
    html = render_to_string("detalle.html", {"user": 'Darwin'}) #obtenemos la plantilla
    pdf = pisa.pisaDocument( html , result) # convertimos en pdf la template
    return HttpResponse(result.getvalue(), content_type='application/pdf')

def compraExitosa(request):
    return render_to_response('compraExitosa.html')

def login(request):
    """view del login
        """
    # Verificamos que los datos lleguen por el methodo POST

    if request.method == 'POST':
        # Cargamos el formulario (ver forms.py con los datos del POST)
        validator = FormLoginValidator(request.POST)
        # Verificamos que los datos esten correctos segun su estructura

        if validator.is_valid():
            # Capturamos las variables que llegan por POST
            usuario = request.POST['usuario']
            clave = request.POST['clave']
            auth.login(request, validator.acceso)  # Crear una sesion
            return HttpResponseRedirect('indexMaster')

        else:
            return render_to_response('login.html', {'error': validator.getMessage()},
                                      context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))

@login_required(login_url="/login")
def master(request):
    marcas = marca.objects.all()
    perfumes = perfume.objects.all()
    InfoFormulario= {'markas': marcas, 'perfumes': perfumes }
    
    if request.method == 'POST':
        if request.POST['sel1'] == 'mr':
            marka = marca()
            marka.nombre = request.POST['nombre']
            marka.imagen = request.FILES['imagen']
            marka.generoPrincipal = request.POST['generoPrincipal']
            marka.generoSecundario = request.POST['generoSecundario']
            marka.save()
            return render_to_response('master.html', InfoFormulario, context_instance=RequestContext(request))
        if request.POST['sel1'] == 'vf':
            perfumes = perfume()
            perfumes.nombre = request.POST['nombreP']
            perfumes.precio = request.POST['precioP']
            perfumes.imagen = request.FILES['imagenP']
            perfumes.presentacion = request.POST['presentacionP']
            perfumes.marca_id = request.POST['marcaP']
            perfumes.generoPrincipal = request.POST['generoPrincipalP']
            perfumes.generoSecundario = request.POST['generoSecundarioP']
            perfumes.save()
            return render_to_response('master.html',InfoFormulario, context_instance=RequestContext(request))

        if request.POST['sel1'] == 'rc':
            
            per = perfume.objects.get( request.POST[perfume.id])
            per.precio = request.POST['precioM']
            per.save()
            
            return render_to_response('master.html',InfoFormulario, context_instance=RequestContext(request))
    else:
            return render_to_response('master.html',InfoFormulario, context_instance=RequestContext(request))

@login_required(login_url="/login")
def registroUsuario(request):
    error = False

    if request.method == 'POST':

        validator = FormRegistroValidator(request.POST)
        validator.required = ['nombre', 'apellidos', 'cedula', 'email', 'password', 'perfil']

        if validator.is_valid():
            usuario = User()
            usuario.first_name = request.POST['nombre']
            usuario.last_name = request.POST['apellidos']
            usuario.username = request.POST['cedula']
            usuario.email = request.POST['email']
            usuario.password = make_password(request.POST['password'])
            tipo = request.POST['perfil']
            #TODO: ENviar correo electronico para confirmar cuenta
            usuario.is_active = True
            perfil = Group.objects.get(id = tipo)
            usuario.save()
            usuario.groups.add(perfil)
            usuario.save()
            return render_to_response('usuario.html', {'success': True}, context_instance=RequestContext(request))
        else:
            return render_to_response('usuario.html', {'error': validator.getMessage()},
                                  context_instance=RequestContext(request))
    # Agregar el usuario a la base de datos
    return render_to_response('usuario.html', context_instance=RequestContext(request))

@login_required(login_url="/login")
def indexMaster(request):
    return render_to_response('indexMaster.html')

@login_required(login_url="/login") # Protegemos la vista con el decorador del loguin para que solo pueda ingresar un usuario logueado
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")
