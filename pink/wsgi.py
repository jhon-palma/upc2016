"""
WSGI config for pink project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

#modo desarrollo 

#from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pink.settings")

#application = get_wsgi_application()

#modo produccion
#import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pink.settings")
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())