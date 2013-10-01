# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from itempage.models import Item

def item_page_display(request, item_id):
    item = Item.objects.get(id=item_id)
    t = loader.get_template('page/item.html')
    c = Context(
        {'item':item}
    )

    return HttpResponse(t.render(c))

