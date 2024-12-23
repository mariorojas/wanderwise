from django.core.management import BaseCommand
from haystack.query import SearchQuerySet

from ...models import Campaign
from ...utils import update_campaign_statistics, update_keyword_statistics


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.queryset = SearchQuerySet()

    def handle(self, *args, **options):
        self.stdout.write('Updating campaign statistics...')

        campaigns = Campaign.objects.all()

        for campaign in campaigns:
            update_campaign_statistics(campaign)

            for keyword in campaign.keywords.all():
                update_keyword_statistics(keyword)

        self.stdout.write('Statistics updated successfully!')
