from haystack import indexes
from . import models


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    visible = indexes.BooleanField(model_attr='visible')

    def get_model(self):
        return models.Document
