# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from models import Item

def item_page_display(request,item_id):
    # item_idに該当するオブジェクトを取得する
    item = Item.objects.get(id=item_id)
    # テンプレートを取得して、モデルの値とマージする
    t = loader.get_template('page/item.html')
    c = Context(
        {'item':item }
    )
    # HTTP Responseを返す。
    return HttpResponse(t.render(c))

