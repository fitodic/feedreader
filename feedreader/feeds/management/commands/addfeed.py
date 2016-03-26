from django.core.management.base import BaseCommand, CommandError
from feeds.models import Feed, Entry, Author
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from bs4 import BeautifulSoup
import feedparser
import datetime

class Command(BaseCommand):
    """docstring for Command"""

    def add_arguments(self, parser):
        parser.add_argument('feed', nargs='?', type=str)

    def handle(self, *args, **options):
        """ Parse the input feed and save the feed, the authors and the entries to the database. """

        # Parse feed
        parsed_feed = feedparser.parse(options['feed'])
        # Create a new Feed object
        try:
            new_feed = Feed.objects.get(title=parsed_feed.feed.title)
        except Feed.DoesNotExist:
            new_feed = Feed.create(title=parsed_feed.feed.title,
                                   url=parsed_feed.feed.link)
            new_feed.save()

        self.stdout.write(
            self.style.SUCCESS('Parsing feed: {0}'.format(new_feed.title)))

        # Parse entry
        for entry in parsed_feed.entries:

            try:
                # Entry already present, skip it
                new_entry = Entry.objects.get(title=entry.title,
                    url=entry.link)
                continue
            except Entry.DoesNotExist:
                # Create a new entry
                new_entry = Entry.create(title=entry.title,
                    published=datetime.datetime(*entry.published_parsed[:6]),
                    url=entry.link, feed=new_feed)
                new_entry.save()

            # Find an image
            try:
                soup = BeautifulSoup(entry.summary, 'html.parser')
                img_link = soup.find('img').get('src')
                # If an image exists, save it
                if img_link:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(urlopen(img_link).read())
                    img_temp.flush()
                    new_entry.image.save('entry_{0}'.format(new_entry.id), ImageFile(img_temp))
                pass
            except AttributeError:
                # No images in summary
                pass

            # Some entries do not contain information about authors
            if entry.has_key('authors'):
                for author in entry.authors:
                    try:
                        new_author = Author.objects.get(name=author.name)
                    except Author.DoesNotExist:
                        new_author = Author.create(name=author.name)
                        new_author.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                'Added author: {0}'.format(new_author.name)))

            else:
                # When no author is specified
                try:
                    new_author = Author.objects.get(name='Unspecified')
                except Author.DoesNotExist:
                    new_author = Author.create(name='Unspecified')
                    new_author.save()


            new_entry.authors.add(new_author)

            self.stdout.write(
                self.style.SUCCESS(
                    'Added entry: {0}'.format(new_entry.title)))
