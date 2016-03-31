from django.test import TestCase
from django.core.urlresolvers import reverse
from . import models
import feedparser


def create_test_data(limit=None):
    """ Test the migration process on lifehacker.com RSS feed. """
    # Test URL
    test_url = 'http://feeds.gawker.com/lifehacker/full'

    parsed_feed = feedparser.parse(test_url)
    feed = models.Feed.save_feed_data(url=test_url)
    step = 0

    for entry in parsed_feed.entries:
        # Create an Entry object
        entry_object = models.Entry.save_entry_data(entry=entry, feed=feed)
        if not entry_object:
            # Entry already present, skip it
            continue
        # Add authors to entries
        author_object = models.Author.save_author_data(
            entry_parsed=entry, entry_object=entry_object)

        if limit and step < limit:
            step += 1
        elif limit:
            break


class FeedsMigrationTests(TestCase):
    """ Test the migration process. """

    def test_migration_process(self):
        """
        This process is used in:
            1. feeds/management/commands/addfeed.py - Command
            2. feeds/views.py - AddFeedView
        The logic is in: feeds/models.py
        WARNING: This test could take about 15 seconds to complete.
        """
        create_test_data(10)


class FeedsViewTests(TestCase):
    """ Test the views of the Feedreader application. """

    def test_empty_index_view(self):
        """ No data should be displayed. """
        response = self.client.get(reverse('feeds:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['list_entries'], [])
        self.assertQuerysetEqual(response.context['list_feeds'], [])

    def test_search_author_view(self):
        """ Test the view for searching authors """
        response = self.client.get(reverse('feeds:author'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter the author's name")

    def test_add_feed_view(self):
        """ Test the view for adding new feeds """
        response = self.client.get(reverse('feeds:addfeed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a unique title for the RSS feed")
        self.assertContains(response, "Enter a unique URL for the RSS feed")

    def test_index_view(self):
        """ The feed and the latest post should be displayed. """
        create_test_data(5)
        feed = models.Feed.objects.first()
        entries = models.Entry.objects.filter(feed=feed)
        response = self.client.get(reverse('feeds:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, feed.title)
        for entry in entries:
            if "'" not in entry.title:
                self.assertContains(response, entry.title)

    def test_feed_view(self):
        """ A specific feed and its latest post should be displayed. """
        create_test_data(5)
        feed = models.Feed.objects.first()
        entries = models.Entry.objects.filter(feed=feed)
        response = self.client.get(reverse('feeds:feed', args=(feed.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, feed.title)
        for entry in entries:
            if "'" not in entry.title:
                self.assertContains(response, entry.title)

    def test_author_view(self):
        """ A specific author and its latest post should be displayed. """
        create_test_data(5)
        author = models.Author.objects.first()
        entries = models.Entry.objects.filter(authors=author)
        response = self.client.get(
            reverse('feeds:authorentries', args=(author.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, author.name)
        for entry in entries:
            if "'" not in entry.title:
                self.assertContains(response, entry.title)
