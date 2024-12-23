from django.contrib.auth.mixins import LoginRequiredMixin


class CampaignRelatedMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.campaign:
            context['campaign'] = self.request.campaign
        return context


class ActiveMenuMixin:
    active_option = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_option'] = self.active_option
        return context