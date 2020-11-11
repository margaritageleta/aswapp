"""aswapp URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from contributions.views import NewsView, NewestView, PublicationView

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('contributions.urls')),
    path(r'', include('users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


"""

urls.py file contains the project level URL information. 
URL is universal resource locator and it provides you with 
the address of the resource (images, webpages, web-applications) 
and other resources for your website.

The main purpose of this file is to connect the web-apps with 
the project. Anything you will be typing in the URL bar will 
be processed by this urls.py file. Then, it will correspond 
your request to the designated app you connected to it.

"""
