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
        if not self.is_valid():
            raise forms.ValidationError(
                self.error_messages['not_RSS'], code='not_RSS')
        feed = feedparser.parse(cleaned_data['url'])
        if 'rss' not in feed.version.lower():
            raise forms.ValidationError(
                self.error_messages['not_RSS'], code='not_RSS')

        return cleaned_data


class AuthorForm(forms.Form):

    error_css_class = 'error'
    required_css_class = 'required'

    error_messages = {
        'no_author': _('No author was found under this name.'),
        'no_name': _('Please type the name of the author'),
    }

    name = forms.CharField(
        max_length=200, label="Author's name", help_text="Enter the author's name")

    def clean(self):

        if not self.is_valid():
            raise forms.ValidationError(
                self.error_messages['no_name'], code='no_name')

        cleaned_data = super(AuthorForm, self).clean()
        try:
            author = models.Author.objects.filter(
                    name__contains=cleaned_data['name'])
            if author.count() == 0:
                raise models.Author.DoesNotExist
        except models.Author.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['no_author'], code='no_author')
