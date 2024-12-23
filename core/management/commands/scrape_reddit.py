import asyncio
import time

import asyncpraw
from asgiref.sync import sync_to_async
from asyncpraw.exceptions import RedditAPIException
from django.conf import settings
from django.core.management import BaseCommand
from django.db.models.functions import Lower
from tqdm.asyncio import tqdm_asyncio, tqdm

from ...models import Keyword, Mention


class Command(BaseCommand):
    """
    Command to scrape Reddit posts for specific keywords
    and save new mentions into the database.
    """

    def __init__(self):
        super().__init__()
        self.mentions_data = {}
        self.existing_titles = set()

    def handle(self, *args, **options):
        asyncio.run(self._handle(*args, **options))

    async def _handle(self, *args, **options):
        self.stdout.write('Starting Reddit scraping...')

        async with asyncpraw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                user_agent=settings.REDDIT_USER_AGENT,
        ) as reddit:
            self.subreddit = await reddit.subreddit('all')

            # limit reddit api concurrent requests
            self.semaphore = asyncio.Semaphore(30)

            keywords = await self._get_unique_keywords_from_db()

            tasks = [self._fetch_posts_for_keyword(keyword) for keyword in keywords]
            await tqdm_asyncio.gather(*tasks, desc='Processing keywords')

            mentions = await self._filter_mentions()
            await self._save_mentions(mentions)

        self.stdout.write('Reddit scraping completed successfully!')

    async def _get_unique_keywords_from_db(self):
        return await sync_to_async(list)(
            Keyword.objects
            .annotate(lower_keyword=Lower('keyword'))
            .values_list('lower_keyword', flat=True)
            .distinct()
        )

    async def _fetch_posts_for_keyword(self, keyword):
        async with self.semaphore:
            try:
                async for submission in self.subreddit.search(
                        keyword, sort='new', limit=settings.REDDIT_MAX_NUM_OF_RESULTS
                ):
                    if not submission.is_self:
                        continue

                    title = submission.title.lower()
                    if title in self.existing_titles:
                        continue

                    self.existing_titles.add(title)
                    self.mentions_data[submission.id] = Mention(
                        external_id=submission.id,
                        title=submission.title,
                        content=submission.selftext[:10000],
                        author=submission.author.name,
                        external_url=submission.url,
                        created_utc=submission.created_utc,
                        mention_type=Mention.REDDIT,
                    )
            except RedditAPIException as e:
                if e.status == 429:
                    self.stdout.write(f'Rate limit hit for "{keyword}", retrying...')
                    await asyncio.sleep(10)
                    await self._fetch_posts_for_keyword(keyword)
                else:
                    self.stdout.write(f'Reddit API error for "{keyword}": {e}')
            except Exception as e:
                self.stdout.write(f'Error fetching keyword "{keyword}": {e}')

    async def _filter_mentions(self):
        existing_ids = await sync_to_async(self._get_existing_mentions_by_ids)()
        return [
            mention for id_, mention in self.mentions_data.items()
            if id_ not in existing_ids
        ]

    def _get_existing_mentions_by_ids(self):
        return list(
            Mention.objects
            .filter(external_id__in=self.mentions_data.keys())
            .values_list('external_id', flat=True)
        )

    async def _save_mentions(self, mentions):
        if not mentions:
            self.stdout.write('No new mentions to save.')
            return

        for mention in tqdm(mentions, desc='Saving mentions'):
            try:
                await sync_to_async(mention.save)()
            except Exception as e:
                self.stdout.write(f'Error saving mention "{mention.external_id}": {e}')
                time.sleep(1)
