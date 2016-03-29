from django.db import models
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.files.temp import NamedTemporaryFile
from django.core.files.images import ImageFile
from bs4 import BeautifulSoup
import urllib
import feedparser
import datetime


class Feed(models.Model):
    """The Feed class"""

    title = models.CharField(max_length=50, unique=True)
    url = models.URLField(max_length=200, unique=True)

    @classmethod
    def create(cls, title, url):
        """ Create a Feed object. """
        feed = cls(title=title, url=url)
        return feed

    @classmethod
    def save_feed_data(cls, url, title=None):
        """ Parse the feed and save it. """
        feed_parsed = feedparser.parse(url)
        if not title:
            # Used when submitting data through the command line tool
            try:
                feed = cls.objects.get(title=feed_parsed.feed.title)
            except cls.DoesNotExist:
                feed = cls.create(title=feed_parsed.feed.title,
                                  url=feed_parsed.href)
                feed.save()
        else:
            # Data verified by the FeedForm
            feed = cls.create(title=title, url=url)
            feed.save()

        return feed

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return HttpResponseRedirect(
            reverse('feeds:feed', kwargs={'feed_id': int(self.id)}))

    class Meta:
        ordering = ['title']


class Author(models.Model):
    """The Author class"""

    name = models.CharField(
        max_length=200, unique=True, blank=True, default='')

    @classmethod
    def create(cls, name):
        """ Create a Author object. """
        author = cls(name=name)
        return author

    @classmethod
    def save_author_data(cls, entry_parsed, entry_object):
        """ Parse the entry and save the authors. """
        if entry_parsed.has_key('authors'):
            # One or multiple authors
            for author in entry_parsed.authors:
                try:
                    new_author = cls.objects.get(name=author.name)
                except cls.DoesNotExist:
                    new_author = cls.create(name=author.name)
                    new_author.save()
                entry_object.authors.add(new_author)
        else:
            # When no author is specified
            try:
                new_author = cls.objects.get(name='Unspecified')
            except cls.DoesNotExist:
                new_author = cls.create(name='Unspecified')
                new_author.save()
            entry_object.authors.add(new_author)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return HttpResponseRedirect(
            reverse('feeds:authorentries', kwargs={'author_id': int(self.id)}))


class Entry(models.Model):
    """The Entry class"""

    title = models.CharField(max_length=100, unique=True)
    published = models.DateTimeField()
    url = models.URLField(max_length=200, unique=True)
    authors = models.ManyToManyField(Author)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='entry_images/', null=True)
    image_url = models.URLField(max_length=200, null=True)

    @classmethod
    def create(cls, title, published, url, feed, image_url):
        """ Create a Entry object. """
        entry = cls(
            title=title, published=published, url=url, feed=feed, image_url=image_url)
        return entry

    @classmethod
    def save_entry_data(cls, feed, entry):
        """ Parse the entry and save it. """

        # Find an image and save its link
        try:
            soup = BeautifulSoup(entry.summary, 'html.parser')
            img_link = soup.find('img').get('src')
        except (urllib.error.URLError, AttributeError):
            # No img tag
            img_link = None

        try:
            # Entry already present, skip it
            new_entry = cls.objects.get(title=entry.title,
                                        url=entry.link)
            return
        except cls.DoesNotExist:
            # Create a new entry
            new_entry = cls.create(title=entry.title,
                published=datetime.datetime(*entry.published_parsed[:6]),
                url=entry.link, feed=feed, image_url=img_link)
            new_entry.save()

        # If there is an image, save it
        if img_link:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib.request.urlopen(img_link).read())
            img_temp.flush()
            new_entry.image.save('entry_{0}'.format(new_entry.id), ImageFile(img_temp))

        return new_entry

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published']
