# Create your views here.
from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponse
# from django.template import Context, loader
from itempage.models import Item
from itempage.forms import ItemSearchForm
from itempage.cart import CartItem

def item_page_display(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    return render(
        request, 'page/item.html',
        {'item':item}
    )

def item_search(request):
    if request.method == 'POST':
        form = ItemSearchForm(request.POST)
        if form.is_valid():
            items = Item.objects.filter(item_name=form.cleaned_data['item_name'])
            return render(
                request, 'page/item_search.html',
                {'form':form, 'items':items}
            )
    else:
        form = ItemSearchForm()

    return render(
        request, 'page/item_search.html',
        {'form':form}
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
    request.session['cart_item_list'] = list(cart_item_list)

    return render(
        request, 'page/cart_item_list.html',
        {'cart_item_list':cart_item_list}
    )
