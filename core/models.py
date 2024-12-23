import random

from django.conf import settings
from django.db import models

SLUG_CHOICES = 'abcdefghijkmnopqrstuvwxyz1234567890'


def generate_unique_slug(length=4):
    slug = ''.join(random.choice(SLUG_CHOICES) for _ in range(length))
    if not Campaign.objects.filter(slug=slug).exists():
        return slug
    return generate_unique_slug(length + 1)


class Campaign(models.Model):
    slug = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    url = models.URLField(blank=True, null=True)
    num_of_mentions = models.IntegerField(default=0)
    num_of_replies = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaigns'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)


class KeywordManager(models.Manager):
    def create_multiple(self, keywords=None, campaign=None):
        objects = [Keyword(keyword=keyword, campaign=campaign) for keyword in keywords]
        return self.bulk_create(objects)

    def keyword_exists(self, keyword=None, campaign=None):
        return super().get_queryset().filter(
            keyword__iexact=keyword,
            campaign=campaign
        ).exists()


class Keyword(models.Model):
    keyword = models.CharField(max_length=200)
    num_of_mentions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='keywords'
    )

    objects = KeywordManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['keyword', 'campaign'],
                name='unique_keyword_campaign'
            ),
        ]

    def __str__(self):
        return self.keyword


class Mention(models.Model):
    FACEBOOK = 'fb'
    LINKEDIN = 'li'
    OTHER = 'other'
    REDDIT = 'rd'
    TWITTER = 'tw'

    MENTION_TYPE = {
        FACEBOOK: 'Facebook',
        LINKEDIN: 'LinkedIn',
        REDDIT: 'Reddit',
        TWITTER: 'X (Twitter)',
    }

    external_id = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(max_length=10000)
    author = models.CharField(max_length=30)
    external_url = models.URLField()
    created_utc = models.BigIntegerField(blank=True, null=True)
    mention_type = models.CharField(max_length=5, choices=MENTION_TYPE, default=OTHER)
    created_at = models.DateTimeField(auto_now_add=True)
