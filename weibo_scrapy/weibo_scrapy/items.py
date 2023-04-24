# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from app01.models import HotSearch,Text,Comment
from scrapy_djangoitem import DjangoItem


class HotSearchItem(DjangoItem):
    django_model = HotSearch

class TextItem(DjangoItem):
    django_model = Text

class CommentItem(DjangoItem):
    django_model = Comment