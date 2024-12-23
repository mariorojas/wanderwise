from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from ..forms import CampaignForm, CampaignEditForm
from ..mixins import ActiveMenuMixin
from ..models import Campaign


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    success_message = 'Your campaign was created successfully.'

    def get_success_url(self):
        return reverse(
            'mention-list',
            kwargs={'campaign_slug': self.object.slug}
        )

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CampaignDeleteView(ActiveMenuMixin, DeleteView):
    model = Campaign
    success_url = reverse_lazy('dashboard')
    active_option = 'settings'

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)


class CampaignSettingsView(ActiveMenuMixin, UpdateView):
    model = Campaign
    form_class = CampaignEditForm
    template_name_suffix = '_settings_form'
    active_option = 'settings'

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('campaign-settings', kwargs={'slug': self.object.slug})
