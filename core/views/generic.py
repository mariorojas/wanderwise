from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.views.generic import TemplateView

from ..mixins import ActiveMenuMixin


class DashboardView(LoginRequiredMixin, ActiveMenuMixin, TemplateView):
    template_name = 'core/dashboard.html'
    active_option = 'dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaigns'] = self.request.user.campaigns.order_by(Lower('name'))
        return context