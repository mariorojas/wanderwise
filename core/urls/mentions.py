from django.urls import path

from ..views import mentions

urlpatterns = [
    path('', mentions.MentionListView.as_view(), name='mention-list'),
]