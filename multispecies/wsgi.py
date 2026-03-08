"""
WSGI config for multispecies project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

os.environ['PYTHON_EGG_CACHE'] = '/tmp'

path = '/opt/webapps'
if path not in sys.path:
    sys.path.append(path)


path = '/opt/webapps/fishing'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multispecies.settings')

application = get_wsgi_application()
