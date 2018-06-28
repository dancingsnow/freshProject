# coding:utf-8
from haystack import indexes
from .models import *


class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsInfo   # 这里写自己想要检索的在models.py中定义的模型类的名字

    def index_queryset(self, using=None):
        return self.get_model().objects.all()