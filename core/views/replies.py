from django.views.generic import TemplateView

from ..mixins import ActiveMenuMixin, CampaignRelatedMixin


class ReplyListView(CampaignRelatedMixin, ActiveMenuMixin, TemplateView):
    template_name = 'core/reply_list.html'
    active_option = 'replies'