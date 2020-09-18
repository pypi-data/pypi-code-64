# pylint: skip-file
"""idcdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import urllib.parse

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import path
from django.urls import reverse
from django.views.generic import TemplateView

from iam.ext.idc.ctrl import AuthenticationCtrl


# https://stackoverflow.com/questions/6779265/how-can-i-not-use-djangos-admin-login-view/13186337
admin.site.login = login_required(admin.site.login)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    AuthenticationCtrl.as_namespace('auth/'),
]
