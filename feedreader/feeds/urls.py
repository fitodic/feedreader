from django.conf.urls import url
from . import views


app_name = 'feeds'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<feed_id>[0-9]+)/$', views.FeedEntryList.as_view(), name='feed'),
]
