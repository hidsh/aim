# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Item(models.Model):
    item_code = models.CharField('商品コード', max_length=256, unique=True)
    item_name = models.CharField('商品名', max_length=256)
    price = models.PositiveIntegerField('価格')
    start_date = models.DateField('掲載開始日', null=True)

    def __unicode__(self):
        return self.item_code

    class Meta:
        db_table = 'item'


