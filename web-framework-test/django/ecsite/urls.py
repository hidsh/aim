from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ecsite/', include('ecsite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^item/(?P<item_id>\d+)/$', 'ecsite.itempage.views.item_page_display'),
    (r'^itemsearch', 'ecsite.itempage.views.item_search'),
    (r'^cart', 'ecsite.itempage.views.do_cart'),
)
