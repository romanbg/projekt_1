"""chargedensity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from constconv import views
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload', views.upload_file, name="upload"),
    path('cif', views.cif, name="cif-file"),
    path('hydrogen', views.hydrogen, name='hydrogen-file'),
    path('hkl', views.hkl, name='hkl-file'),
    path('structure_factor', views.StructureFactorView.as_view(), name='structure-factor'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
        serve, {'document_root':settings.MEDIA_ROOT,}),]
