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
