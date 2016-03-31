# FeedReader

A Django application for saving RSS feeds and their entries.

### Setup:
Download the source code and create the SQLite database by running
```bash
$ python manage.py migrate
```
**Warning:**
In the event the migration process does not create a migration for a specific app (e.g. thumbnail), run
```bash
$ python manage.py makemigrations thumbnail
```
and repeat the *migrate* command.

### Usage:
Navigate to the directory that contains the *manage.py* file and run:
```bash
$ python manage.py runserver
```
Open a Web browser and visit the [site](http://localhost:8000/feeds/).
New  feeds can be added using the [UI](http://localhost:8000/feeds/addfeed/) or the command line:
```bash
$ python manage.py addfeed http://feeds.gawker.com/lifehacker/full
```

### Tests:
To test the provided functionality, run:
```bash
$ python manage.py test feeds
```
Tests are run using the [Lifehacker RSS feed](http://feeds.gawker.com/lifehacker/full) as a reference.
The application was tested using the following RSS feeds:
1. [Lifehacker](http://feeds.gawker.com/lifehacker/full)
2. [Ubuntu](https://insights.ubuntu.com/feed/)
3. [Fedora](https://fedoramagazine.org/feed/)
4. [Python](https://www.python.org/dev/peps/peps.rss/)

### Requirements:
All the requirements are listed in the *requirements.py* file. This project was developed using **Python 3**.