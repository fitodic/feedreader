from django.core.management.base import BaseCommand, CommandError
from feeds import models
import feedparser

class Command(BaseCommand):
    """The Command class"""

    def add_arguments(self, parser):
        parser.add_argument('feed', nargs='?', type=str)

    def handle(self, *args, **options):
        """ Parse the input feed and save the feed, the authors and the
            entries to the database. """

        # Parse feed
        parsed_feed = feedparser.parse(options['feed'])
        # Create a Feed object
        feed = models.Feed.save_feed_data(url=options['feed'])

        self.stdout.write(
            self.style.SUCCESS('Parsing feed: {0}'.format(feed.title)))

        # Parse entry
        for entry in parsed_feed.entries:
            # Create an Entry object
            entry_object = models.Entry.save_entry_data(entry=entry, feed=feed)
            if not entry_object:
                # Entry already present, skip it
                continue
            # Add authors to entries
            author_object = models.Author.save_author_data(
                entry_parsed=entry, entry_object=entry_object)

            self.stdout.write(
                self.style.SUCCESS(
                    'Added entry: {0}'.format(entry_object.title)))
