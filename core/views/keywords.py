from django.db.models.functions import Lower
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, FormView, ListView

from ..forms import KeywordForm, KeywordUrlForm
from ..mixins import ActiveMenuMixin, CampaignRelatedMixin
from ..models import Keyword


class KeywordCreateView(CampaignRelatedMixin, ActiveMenuMixin, CreateView):
    model = Keyword
    form_class = KeywordForm
    active_option = 'keywords'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['campaign'] = self.request.campaign
        return kwargs

    def form_valid(self, form):
        form.instance.campaign = self.request.campaign
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'keyword-list', kwargs={'campaign_slug': self.object.campaign.slug}
        )


class KeywordDeleteView(CampaignRelatedMixin, ActiveMenuMixin, DeleteView):
    model = Keyword
    active_option = 'keywords'

    def get_queryset(self):
        return self.request.campaign.keywords

    def get_success_url(self):
        return reverse(
            'keyword-list', kwargs={'campaign_slug': self.object.campaign.slug}
        )


class KeywordListView(CampaignRelatedMixin, ActiveMenuMixin, ListView):
    model = Keyword
    active_option = 'keywords'

    def get_queryset(self):
        queryset = self.request.campaign.keywords
        return queryset.order_by(Lower('keyword'))


class KeywordUrlCreateView(CampaignRelatedMixin, ActiveMenuMixin, FormView):
    form_class = KeywordUrlForm
    template_name = 'core/keyword_url_form.html'
    active_option = 'keywords'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['campaign'] = self.request.campaign
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'keyword-list', kwargs={'campaign_slug': self.request.campaign.slug}
        )
