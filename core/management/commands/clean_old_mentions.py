from django.core.management import BaseCommand, call_command
from haystack.query import SearchQuerySet
from tqdm import tqdm

from ...models import Mention


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.queryset = SearchQuerySet()

    def handle(self, *args, **options):
        mentions = Mention.objects.all()

        for mention in tqdm(mentions, 'Deleting mentions'):
            mention.delete()

        self.stdout.write(f'Mentions cleaned successfully')

        call_command('update_statistics')
