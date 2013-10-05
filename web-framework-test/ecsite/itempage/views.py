# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page
from models import Item
from ecsite.itempage.forms import ItemSearchForm
from ecsite.itempage.cart import CartItem

@cache_page(60 * 15)            # 単位は秒。15分キャッシュする。
def item_page_display(request,item_id):
    item = get_object_or_404(Item, id=item_id)

    return direct_to_template(request, 'page/item.html',
                              extra_context={'item':item}
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

def do_cart(request):
    item_id = int(request.POST['item_id'])
    item = Item.objects.get(id=item_id)

    cart_item_list = request.session.get('cart_item_list', [])
    ci = CartItem()
    ci.item_id = item_id
    ci.item_code = item.item_code
    ci.item_name = item.item_name
    ci.price = item.price
    ci.buy_num = request.POST['buy_num']
    cart_item_list.append(ci)
    request.session['cart_item_list'] = cart_item_list

    return direct_to_template(request, "page/cart_item_list.html",
                              extra_context={
                                'cart_item_list':cart_item_list,
                              }
    )
