from django.conf.urls.defaults import *
from hello_view import hello, plaintext_time, redirect_to_googlemap, your_ip_address, greet_with_form_data, reverse_url_bit, url_sum, show_metadata, show_metadata_with_load_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^greet/$', hello),
    (r'^time/$', plaintext_time),
    (r'^map/(\d+)/(\d+)/', redirect_to_googlemap),
    (r'^ip_addr/$', your_ip_address),
    (r'^formdata/$', greet_with_form_data),
    (r'^reversed/(?P<bit>.*)/$', reverse_url_bit),
    (r'sum/(\d+)/(\d+)/$', url_sum),
    (r'meta/$', show_metadata),
    (r'load/$', show_metadata_with_load_template),
)
