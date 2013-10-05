# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from models import Item

def item_page_display(request,item_id):
    item = get_object_or_404(Item, id=item_id)

    return direct_to_template(request, 'page/item.html',
                              extera_content={'item':item}
    )
