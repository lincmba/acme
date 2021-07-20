"""acme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django_eventstream
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, reverse_lazy, include
from django.views.generic.base import RedirectView

from acme.products.views import stream_import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    url(r'^events/(?P<task_id>[\w-]+)/', include(django_eventstream.urls), {
        'format-channels': ['{task_id}']
    }),
    url(r'^events/(?P<task_id>[\w-]+)/livestream', stream_import),
    url(r'^events/', include(django_eventstream.urls)),
]
admin.site.site_header = "ACME"
admin.site.site_title = "Acme Inc"
admin.site.index_title = "Welcome to Acme Inc Admin Portal"
