"""
WSGI config for guest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import django
import django.core.handlers.wsgi

from django.core.wsgi import get_wsgi_application
django.setup()


sys.path.append('D:/Learn/guest')
sys.path.append('D:/Learn/guest/guest')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guest.settings")

# application = get_wsgi_application()



application = django.core.handlers.wsgi.WSGIHandler()