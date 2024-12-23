from datetime import datetime

from haystack import indexes

from .models import Keyword, Mention


class KeywordIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    keyword = indexes.CharField(model_attr='keyword')

    def get_model(self):
        return Keyword

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class MentionFullIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    external_id = indexes.CharField(model_attr='external_id')
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    author = indexes.CharField(model_attr='author')
    external_url = indexes.CharField(model_attr='external_url')
    created_utc = indexes.IntegerField(model_attr='created_utc')
    created_datetime = indexes.DateTimeField()
    mention_type = indexes.CharField(model_attr='mention_type')
    mention_type_display = indexes.CharField()

    def get_model(self):
        return Mention

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_mention_type_display(self, obj):
        return Mention.MENTION_TYPE.get(obj.mention_type, obj.mention_type)

    def prepare_created_datetime(self, obj):
        return datetime.fromtimestamp(obj.created_utc)
