from django.conf import settings
from haystack.generic_views import SearchView

from ..forms import MentionSearchForm
from ..mixins import ActiveMenuMixin, CampaignRelatedMixin


class MentionListView(CampaignRelatedMixin, ActiveMenuMixin, SearchView):
    active_option = 'mentions'
    form_class = MentionSearchForm
    template_name = 'core/mention_list.html'
    paginate_by = settings.KEYWORDS_PER_PAGE

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_utc')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if not self.request.GET.get('q', None):
            campaign = self.request.campaign
            kwargs['keywords'] = campaign.keywords.values_list('keyword', flat=True)

        return kwargs
