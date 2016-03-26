from django.shortcuts import render
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from . import models


class IndexView(generic.ListView):

    template_name = 'feeds/index.html'
    context_object_name = 'list_entries'
    model = models.Entry
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['list_feeds'] = models.Feed.objects.all()
        return context


class FeedEntryList(generic.ListView):

    template_name = 'feeds/feed_list.html'
    context_object_name = 'list_entries'
    model = models.Entry
    paginate_by = 20

    def get_queryset(self):
        #import ipdb; ipdb.set_trace()
        self.feed = get_object_or_404(models.Feed, id=self.kwargs['feed_id'])
        return models.Entry.objects.filter(feed=self.feed)

    def get_context_data(self, **kwargs):
        context = super(FeedEntryList, self).get_context_data(**kwargs)
        context['feed'] = self.feed
        context['list_feeds'] = models.Feed.objects.all()
        return context

