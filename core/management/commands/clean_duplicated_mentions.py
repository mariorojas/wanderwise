from django.core.management import BaseCommand, call_command
from haystack.query import SearchQuerySet
from tqdm import tqdm

from ...models import Mention


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.queryset = SearchQuerySet()

    def handle(self, *args, **options):
        items_deleted = 0
        titles = set()

        mentions = Mention.objects.all().order_by('-created_utc')

        for mention in tqdm(mentions, desc='Processing mentions'):
            if mention.title in titles:
                mention.delete()
                items_deleted += 1
            else:
                titles.add(mention.title)

        self.stdout.write(f'Mentions cleaned: {items_deleted}')

        call_command('update_statistics')
