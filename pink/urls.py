"""pink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from pinkapp.views import *

urlpatterns = [
    url(r'^$', index , name='index'),
    url(r'^marcas$', marcas , name='marcas'),
    url(r'^indexMaster$', indexMaster , name='indexMaster'),
    url(r'^search$', search , name='search'),
    url(r'^contacto$', contacto , name='contacto'),
    url(r'^comprar$', comprar , name='comprar'),
    url(r'^compraExitosa$', compraExitosa , name='compraExitosa'),
    url(r'^detalle$', verpdf , name='detalle'),
    url(r'^login$', login , name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^master$', master , name='master'),
    url(r'^usuario$', registroUsuario, name='registroUsuario'),
    url(r'^admin/', admin.site.urls),
]
