from django.contrib import admin

from .models import Campaign, Keyword, Mention


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'num_of_mentions', 'owner', 'created_at']


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'campaign', 'num_of_mentions', 'owner', 'created_at']

    @admin.display
    def owner(self, obj):
        return obj.campaign.owner


@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'external_url', 'mention_type']
