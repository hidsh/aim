# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect

def hello(request):
    message = "<html><body>こんにちわ, Django!</body></html>"
    return HttpResponse(message)

def plaintext_time(request):
    from time import ctime
    return HttpResponse(ctime(), mimetype='text/plain')

def hello_error(request):
    raise Http404

def forbidden_page(request):
    return HttpResponseForbidden()

def redirect_to_googlemap(request, latitude, longitude):
    redirect_url = 'http://maps.google.co.jp/?ie=UTF8&ll=%s,%s&z=10' % (latitude, longitude)
    return HttpResponseRedirect(redirect_url)

def your_ip_address(request):
    return HttpResponse(request.META['REMOTE_ADDR'], mimetype='text/plain')

def greet_with_form_data(request):
    given_name  = request.GET['given_name']
    family_name = request.GET['family_name']
    return HttpResponse('Hello, %s %s!' % (given_name, family_name))

def reverse_url_bit(request, bit=''):
    return HttpResponse(reversed(bit), mimetype='text/plain')

def url_sum(request, a, b):
    a_int = int(a)
    b_int = int(b)
    return HttpResponse(str(a_int + b_int), mimetype='text/plain')



from django.template import Template, Context
showmeta_template_string = """
<html>
  <body>
    <table>
      <tr><td>Key</td><td>Value</td></tr>
        {% for item in metadata.items %}
      <tr>
        <td>{{ item.0 }}</td><td>{{ item.1 }}</td>
      </tr>
      {% endfor %}
    </table>
  </body>
</html>
"""
def show_metadata(request):
  template = Template(showmeta_template_string)
  context = Context()
  context.update({'metadata': request.META})
  return HttpResponse(template.render(context))


from django.template import loader
def show_metadata_with_load_template(request):
    context = Context()
    context.update(dict(metadata=request.META))
    template = loader.get_template('showmeta.html')
    return HttpResponse(template.render(context))
    
