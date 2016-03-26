from django.db import models


class Feed(models.Model):
    """The Feed class"""

    title = models.CharField(max_length=50, unique=True)
    url = models.URLField(max_length=200, unique=True)

    @classmethod
    def create(cls, title, url):
        feed = cls(title=title, url=url)
        return feed

    def __str__(self):
        return self.title


class Author(models.Model):
    """The Author class"""

    name = models.CharField(
        max_length=200, unique=True, blank=True, default='')

    @classmethod
    def create(cls, name):
        author = cls(name=name)
        return author

    def __str__(self):
        return self.name


class Entry(models.Model):
    """The Entry class"""

    title = models.CharField(max_length=100, unique=True)
    published = models.DateTimeField()
    url = models.URLField(max_length=200, unique=True)
    authors = models.ManyToManyField(Author)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    image = models.URLField(max_length=200, null=True)

    @classmethod
    def create(cls, title, published, url, feed, image):
        entry = cls(
            title=title, published=published, url=url, feed=feed, image=image)
        return entry

    def __str__(self):
        return self.title
