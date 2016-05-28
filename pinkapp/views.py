# -*- encoding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.template import RequestContext
from .models import marca, perfume
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from validators import FormContacto,FormLoginValidator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth

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


        """
        Manera de realizar consultar por un criterio a la vez
        #buscamos por nombre del curso
        cursos = Course.objects.filter( name__icontains =  request.GET['filter'] )
        # Si no existen resultados buscarmos por precio
        if not cursos.exists():
            cursos = Course.objects.filter( price__icontains =  request.GET['filter'] )
        # Si no existen resultados buscarmos por profesor
        if not cursos.exists():
            cursos = Course.objects.filter( teacher__name__icontains =  request.GET['filter'] )
        filter = request.GET['filter']
        """

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
            return HttpResponseRedirect('master')

        else:
            return render_to_response('index.html', {'error': validator.getMessage()},
                                      context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))

def master(request):
    return render_to_response('master.html')
    