"""
WSGI config for jskills project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/jskills/src/django/jskills/')
sys.path.append('/home/jskills/src/django/jskills/jskills/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jskills.settings')

application = get_wsgi_application()
