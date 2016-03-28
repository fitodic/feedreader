from django.conf.urls import url
from . import views


app_name = 'feeds'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<feed_id>[0-9]+)/$', views.FeedEntryList.as_view(), name='feed'),
    url(r'^addfeed/$', views.AddFeedView.as_view(), name='addfeed'),
    url(r'^author/$', views.AuthorView.as_view(), name='author'),
    url(r'^authorsearch/$', views.AuthorSearchView.as_view(), name='authorsearch'),
    url(r'^author/(?P<author_id>[0-9]+)/$', views.AuthorEntryList.as_view(), name='authorentries'),
]
