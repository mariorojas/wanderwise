from django.urls import path

from ..views import keywords

urlpatterns = [
    path(
        '',
        keywords.KeywordListView.as_view(),
        name='keyword-list'
    ),

    path(
        'new/',
        keywords.KeywordCreateView.as_view(),
        name='new-keyword'
    ),

    path(
        'url/new/',
        keywords.KeywordUrlCreateView.as_view(),
        name='url-new-keyword'
    ),

    path(
        '<int:pk>/delete/',
        keywords.KeywordDeleteView.as_view(),
        name='delete-keyword'
    ),
]
