from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import feedparser
import json
from . import models
from . import forms


class IndexView(generic.ListView):
    """ The IndexView class.
        Displays lists of feeds and entries. """

    template_name = 'feeds/index.html'
    context_object_name = 'list_entries'
    model = models.Entry
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['list_feeds'] = models.Feed.objects.all()
        return context


class FeedEntryList(generic.ListView):
    """ The FeedEntryList class.
        Displays a list of entries for a particular feed. """

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
    """ The AddFeedView class.
        Used for adding new feeds. """

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
            author_object = models.Author.save_author_data(
                entry_parsed=entry, entry_object=entry_object)

        return feed.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(AddFeedView, self).get_context_data(**kwargs)
        context['list_feeds'] = models.Feed.objects.all()
        return context


class AuthorEntryList(generic.ListView):
    """ The AuthorEntryList class.
        Displays a list of entries of a particular author. """

    template_name = 'feeds/author_entry_list.html'
    context_object_name = 'list_entries'
    model = models.Entry
    paginate_by = 20

    def get_queryset(self):
        self.author = get_object_or_404(
            models.Author, id=self.kwargs['author_id'])
        return models.Entry.objects.filter(authors=self.author)

    def get_context_data(self, **kwargs):
        context = super(AuthorEntryList, self).get_context_data(**kwargs)
        context['author'] = self.author
        context['list_feeds'] = models.Feed.objects.all()
        return context


class AuthorView(generic.FormView):
    """ The AuthorView class.
        Used for rendering the author search form and redirecting to the
        AuthorEntryList upon a successful search. """

    template_name = 'feeds/author_search.html'
    form_class = forms.AuthorForm
    model = models.Author

    def form_valid(self, form):
        data = form.cleaned_data
        author = models.Author.objects.get(name__contains=data['name'])
        return author.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context['list_feeds'] = models.Feed.objects.all()
        return context


class AuthorSearchView(generic.FormView):
    """ The AuthorSearchView class.
        Used for sending a list of possible authors as JSON after receiving at
        least two letters. """

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cleaned_data = []
            search_term = request.GET['term']
            query_results = models.Author.objects.filter(
                name__contains=search_term)
            for result in query_results:
                result_json = {}
                result_json['id'] = result.id
                result_json['label'] = result.name
                result_json['value'] = result.name
                cleaned_data.append(result_json)
            json_data = json.dumps(cleaned_data)
            return HttpResponse(json_data, 'application/json')
