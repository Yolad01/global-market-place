
import os
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from main.consumers import EchoConsumer, ChatConsumer

# from yolad.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter([
            re_path(r"ws/chat/(?P<username>[\w.@+-]+)/$", ChatConsumer.as_asgi()),
            path("ws/main/", EchoConsumer.as_asgi())
            
        ])
        ),
    }
)