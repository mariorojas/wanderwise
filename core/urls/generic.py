from django.urls import path

from ..views.generic import DashboardView

urlpatterns = [
    path(
        'dashboard/',
        DashboardView.as_view(),
        name='dashboard'
    ),
]
