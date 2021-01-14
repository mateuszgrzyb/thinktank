"""
ASGI config for thinktank project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thinktank.settings')
django_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from chat.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})


