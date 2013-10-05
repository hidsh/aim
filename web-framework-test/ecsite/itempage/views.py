# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.views.generic.simple import direct_to_template
from models import Item
from ecsite.itempage.forms import ItemSearchForm

def item_page_display(request,item_id):
    item = get_object_or_404(Item, id=item_id)

    return direct_to_template(request, 'page/item.html',
                              extera_content={'item':item}
    )

def item_search(request):
    if request.method == 'POST':
        form = ItemSearchForm(request.POST)
        if form.is_valid():
            items = Item.objects.filter(item_name=form.cleaned_data['item_name'])
            return direct_to_template(request, 'page/item_search.html',
                                      extra_context={
                                        'form':form,
                                        'items':items,
                                      }
            )
    else:
        form = ItemSearchForm() # 初期表示

    return direct_to_template(request, 'page/item_search.html',
                              extra_context={
                                'form':form,
                              }
     )
