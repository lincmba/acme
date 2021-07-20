"""
ASGI config for acme project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

import django_eventstream
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acme.settings')

application = ProtocolTypeRouter({
    'http': URLRouter([
        url(r'^events/(?P<task_id>[\w-]+)/', AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), {'format-channels': ['{task_id}']}),
        url(r'', get_asgi_application()),
    ]),
})
