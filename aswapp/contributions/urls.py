from django.conf.urls import url
from contributions import views


urlpatterns = [
    url(r'news', views.NewsView.as_view(), name='news_view'),
    url(r'newest', views.NewestView.as_view(), name='newest_view'),
    url(r'submit/', views.SubmitView.as_view(), name='submit_contribution'),
    url(r'^item/(?P<id>[0-9A-Za-z_\-]+)/$', views.PublicationView.as_view(), name='show_contribution_view'),
    url (r'^item/(?P<id>[0-9A-Za-z_\-]+)/comment/$', views.CommentView.as_view(), name = 'comment_view')
]
