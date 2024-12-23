from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Campaign, Keyword
from .utils import update_campaign_statistics, update_keyword_statistics


@receiver(post_save, sender=Campaign)
def post_save_campaign_statistics(sender, instance, created, **kwargs):
    if created:
        update_campaign_statistics(instance)


@receiver(post_delete, sender=Keyword)
def post_delete_keyword_statistics(sender, instance, **kwargs):
    update_campaign_statistics(instance.campaign)


@receiver(post_save, sender=Keyword)
def post_save_keyword_statistics(sender, instance, created, **kwargs):
    if created:
        update_keyword_statistics(instance)
        update_campaign_statistics(instance.campaign)
