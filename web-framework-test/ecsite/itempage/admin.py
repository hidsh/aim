# -*- coding: utf-8 -*-
from django.contrib import admin
from ecsite.itempage.models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'item_name', 'price')
    
admin.site.register(Item, ItemAdmin)
# import pdb; pdb.set_trace()


