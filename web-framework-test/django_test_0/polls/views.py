# Create your views here.
# from django.template import Context, loader
from polls.models import Poll
# from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    # t = loader.get_template('polls/index.html')
    # c = Context({
    #         'latest_poll_list':latest_poll_list,
    # })
    # return HttpResponse(t.render(c))
    return render_to_response('polls/index.html', {'latest_poll_list':latest_poll_list})

# from django.http import Http404
def detail(request, poll_id):
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404
    # return render_to_response('polls/detail.html', {'poll':p})

    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll':p})
