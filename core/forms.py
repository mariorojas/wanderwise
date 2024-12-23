import csv

import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from haystack.forms import SearchForm
from tqdm import tqdm

from .models import Campaign, Keyword
from .utils import generate_ai_keywords


class CampaignEditForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'url', 'description']


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'url', 'description']

    def save(self, commit=True):
        super().save(commit)

        keywords_values = generate_ai_keywords(input_=self.instance.description)

        for keywords_value in keywords_values:
            Keyword.objects.create(keyword=keywords_value, campaign=self.instance)

        return self.instance


class KeywordForm(forms.ModelForm):
    keyword = forms.CharField(min_length=4, max_length=settings.MAX_KEYWORD_LENGTH)

    class Meta:
        model = Keyword
        fields = ['keyword']

    def __init__(self, *args, **kwargs):
        self.campaign = kwargs.pop('campaign', None)
        super().__init__(*args, **kwargs)

    def clean_keyword(self):
        keyword = self.cleaned_data['keyword']

        if Keyword.objects.keyword_exists(keyword=keyword, campaign=self.campaign):
            raise ValidationError('This keyword is already registered.')

        return keyword


class KeywordUrlForm(forms.Form):
    url = forms.URLField(
        label='Google Sheets URL',
        help_text='You can add up to 50 keywords. Please list all keywords in the first column.',
    )

    def __init__(self, *args, **kwargs):
        self.campaign = kwargs.pop('campaign', None)
        super().__init__(*args, **kwargs)

    def save(self):
        spreadsheet_id = self._get_spreadsheet_id()
        data = self._fetch_google_sheets_data(spreadsheet_id)

        keywords = list({row[0] for row in data})[:settings.MAX_NUM_OF_KEYWORDS]

        for keyword in tqdm(keywords, desc='Processing keywords'):
            sanitized_keyword = keyword.strip()[:settings.MAX_KEYWORD_LENGTH]

            if not sanitized_keyword:
                continue

            if Keyword.objects.keyword_exists(keyword=keyword, campaign=self.campaign):
                continue

            Keyword.objects.create(keyword=sanitized_keyword, campaign=self.campaign)

    def clean_url(self):
        url = self.cleaned_data['url']

        if not url.startswith(settings.GOOGLE_SHEETS_PREFIX):
            raise ValidationError('Please provide a valid Google Sheets URL.')

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException:
            raise ValidationError(
                'Unable to fetch data from the Google Sheets. Please check the URL and try again.'
            )

        return url

    def _fetch_google_sheets_data(self, spreadsheet_id):
        url = settings.GOOGLE_SHEETS_CSV_URL.format(spreadsheet_id)

        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8')

        return list(csv.reader(content.splitlines()))

    def _get_spreadsheet_id(self):
        url = self.cleaned_data['url']
        try:
            chunks = url.split('/')
            spreadsheet_id_index = chunks.index('d') + 1
            return chunks[spreadsheet_id_index]
        except (ValueError, IndexError):
            raise ValidationError(
                'Invalid Google Sheets URL. Ensure the URL is in the correct format.'
            )


class MentionSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        self.keywords = kwargs.pop('keywords', None)
        super().__init__(*args, **kwargs)

    def no_query_found(self):
        queryset = super().no_query_found()

        if self.keywords:
            queryset = self.searchqueryset.filter(text__in=self.keywords)

        return queryset

    def search(self):
        kwargs = {
            'hl': 'true',
            'hl.fl': 'title,content',
            'hl.method': 'unified',
            'hl.tag.pre': '<b class="text-danger">',
            'hl.tag.post': '</b>',
        }
        return self._search().highlight(**kwargs)

    def _search(self):
        if not self.is_valid():
            return self.no_query_found()

        query = self.cleaned_data.get('q', None)

        if not query:
            return self.no_query_found()

        queryset = self.searchqueryset.filter(text__exact=query)

        return queryset
