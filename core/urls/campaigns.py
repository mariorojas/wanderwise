from django.urls import path

from ..views import campaigns

urlpatterns = [
    path(
        'new/',
        campaigns.CampaignCreateView.as_view(),
        name='new-campaign'
    ),

    path(
        '<slug:slug>/delete/',
        campaigns.CampaignDeleteView.as_view(),
        name='delete-campaign'
    ),

    path(
        '<slug:slug>/settings/',
        campaigns.CampaignSettingsView.as_view(),
        name='campaign-settings'
    ),
]
