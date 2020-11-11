from django.conf.urls import url
from django.urls import path
from users import views


urlpatterns =[
    path(r'register', views.register, name='register_view'),
    path(r'login', views.login, name='login_view'),
    path(r'forgot', views.forgot, name='forgot_view'),
    path(r'logout', views.logout, name='logout_view'),
]