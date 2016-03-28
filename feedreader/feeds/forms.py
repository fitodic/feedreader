from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
import feedparser
from . import models


class FeedForm(forms.ModelForm):

    error_messages = {
        'not_RSS': _("The provided URL is not a valid RSS feed."),
    }

    class Meta:
        model = models.Feed
        fields = ('title', 'url')

    def clean(self):
        cleaned_data = super(FeedForm, self).clean()

        feed = feedparser.parse(cleaned_data['url'])
        if 'rss' not in feed.version.lower():
            raise forms.ValidationError(
                self.error_messages['not_RSS'], code='not_RSS')

        return cleaned_data


class AuthorForm(forms.ModelForm):

    error_messages = {
        'no_author': _('No author was found under this name.'),
        'no_name': _('Please type the name of the author'),
    }

    class Meta:
        model = models.Author
        fields = ('name',)

    def clean(self):
        try:
            if self.cleaned_data['name'] != '':
                author = models.Author.objects.filter(
                    name__contains=self.cleaned_data['name'])
                if author.count() == 0:
                    raise models.Author.DoesNotExist
            else:
                raise forms.ValidationError(
                self.error_messages['no_name'], code='no_name')
        except models.Author.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['no_author'], code='no_author')

        return self.cleaned_data



