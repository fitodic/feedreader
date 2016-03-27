from django.views import generic
from django.shortcuts import get_object_or_404
import feedparser
from . import models
from . import forms


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
        self.feed = get_object_or_404(models.Feed, id=self.kwargs['feed_id'])
        return models.Entry.objects.filter(feed=self.feed)

    def get_context_data(self, **kwargs):
        context = super(FeedEntryList, self).get_context_data(**kwargs)
        context['feed'] = self.feed
        context['list_feeds'] = models.Feed.objects.all()
        return context


class AddFeedView(generic.CreateView):

    template_name = 'feeds/add_feed.html'
    form_class = forms.FeedForm
    model = models.Feed

    def form_valid(self, form):
        # Extract data from the form
        data = form.cleaned_data
        # Parse feed
        feed_parsed = feedparser.parse(data['url'])
        # Create a Feed object
        feed = models.Feed.save_feed_data(title=data['title'], url=data['url'])

        for entry in feed_parsed.entries:
            entry_object = models.Entry.save_entry_data(entry=entry, feed=feed)
            if not entry_object:
                # Entry already present, skip it
                continue
            # Add authors to entries
            author_object = models.Author.save_author_data(entry_parsed=entry, entry_object=entry_object)

        return feed.get_absolute_url()



