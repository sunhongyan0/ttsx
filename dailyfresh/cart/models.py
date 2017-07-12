from django.db import models
from goods.models import GoodsInfo


class CartInfo(models.Model):
    user = models.ForeignKey('user_info.ttsx_info')
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
