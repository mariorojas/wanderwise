from django.urls import path

from ..views import replies

urlpatterns = [
    path(
        '',
        replies.ReplyListView.as_view(),
        name='reply-list'
    ),
]