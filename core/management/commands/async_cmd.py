import asyncio

import asyncpraw
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Hello!')
        asyncio.run(self.async_task())

    async def async_task(self):
        reddit = asyncpraw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT
        )

        self.subreddit = await reddit.subreddit('all')

        print(self.subreddit.display_name)