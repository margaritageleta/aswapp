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
from django.conf.urls import include, url, handler404
from django.conf.urls.static import static
from contributions.views import NewsView, NewestView, PublicationView
from users.views import ProfileView
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#schema_view = get_swagger_view(title='HackerNews API')
schema_view = get_schema_view(
   openapi.Info(
      title="Hackernews API",
      default_version='v1',
      description="This is the Open API documentation for the REST API of our beloved application **HackerNews API** deployed at <https://hackernews-project.herokuapp.com/api>. <br>All operations are executable. The operations that requires authentication: `deletePost`, `updateUser` and `deleteComment`. In this case, you must **Authorize** your request by providing the api_key vaule you got when you created the tweet.",
      terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@snippets.local"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    
    path(r'admin/', admin.site.urls),
    path(r'', include('contributions.urls')),
    path(r'', include('users.urls')),
    #url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    path(r'api/items/', include('contributions.api.urls')),
    path(r'api/users/', include('users.api.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
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
