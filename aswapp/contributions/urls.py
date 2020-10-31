from django.conf.urls import url
from contributions import views


urlpatterns = [
    url(r'news', views.news_view, name='news_view'),
    url(r'newest', views.newest_view, name='newest_view'),
    url(r'submit/', views.SubmitView.as_view(), name='submit_contribution'),
    url(r'^(?P<kind>[-\w]+)/(?P<id>[0-9A-Za-z_\-]+)/$', views.show_contribution_view, name='show_contribution_view'),
]
