from django.conf.urls import url
from contributions import views


urlpatterns = [
    url(r'news', views.news_view, name='News view'),
    url(r'newest', views.newest_view, name='Newest view'),
    url(r'submit/', views.SubmitView.as_view(), name='submit_contribution')
   
]