from django.conf import settings
from haystack.query import SearchQuerySet


def generate_ai_keywords(input_=None):
    if settings.ENABLE_AI_KEYWORDS:
        return ['artificial intelligence', 'technology', 'python', 'machine learning']
    return []


def update_campaign_statistics(campaign):
    keyword_values = campaign.keywords.values_list('keyword', flat=True)
    campaign.num_of_mentions = SearchQuerySet().filter(text__in=keyword_values).count()
    campaign.save()


def update_keyword_statistics(keyword):
    keyword_value = keyword.keyword
    keyword.num_of_mentions = SearchQuerySet().filter(text__exact=keyword_value).count()
    keyword.save()
