"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import dotenv
from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv()

settings_module_name = os.environ.get('SETTINGS_MODULE_NAME')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'core.settings.{settings_module_name}')

application = get_wsgi_application()
