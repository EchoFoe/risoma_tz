import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risoma_tz.settings')

application = get_wsgi_application()
