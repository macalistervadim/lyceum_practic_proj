import os

import django.core.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lyceum.settings")

application = django.core.asgi.get_asgi_application()
