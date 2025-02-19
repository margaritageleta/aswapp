from django.conf.urls import url

from contributions.api import views


urlpatterns = [
    url(r'^$', views.ItemsListAPIView.as_view(), name='items'),
    url(r'^asks/$', views.ItemsAsksListAPIView.as_view(), name='asks'),
    url(r'^urls/$', views.ItemUrlsListAPIView.as_view(), name='urls'),
    #url(r'^comments/$', views.CommentListAPIView.as_view(), name='comments'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/$', views.ItemAPIView.as_view(), name='item'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/votes/$', views.ItemVotesAPIView.as_view(), name='vote_item'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/comments/$', views.ItemCommentsListAPIView.as_view(), name='item_comments'),
    url(r'^comments/(?P<id>[0-9A-Za-z_\-]+)/$', views.CommentAPIView.as_view(), name='comment'),
    url(r'^comments/(?P<id>[0-9A-Za-z_\-]+)/votes/$', views.CommentVotesAPIView.as_view(), name='comment'),

]