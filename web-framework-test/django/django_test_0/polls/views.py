# Create your views here.
# from django.template import Context, loader
from polls.models import Poll, Choice
# from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
"""
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    # t = loader.get_template('polls/index.html')
    # c = Context({
    #         'latest_poll_list':latest_poll_list,
    # })
    # return HttpResponse(t.render(c))
    return render_to_response('polls/poll_list.html', {'latest_poll_list':latest_poll_list})

# from django.http import Http404
def detail(request, poll_id):
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404
    # return render_to_response('polls/detail.html', {'poll':p})

    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll':p})
"""

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render_to_response('polls/poll_detail.html', {
                  'object':p,
                  'error_message':'選択肢を選んでいません。',
                })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

"""
def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll':p})
"""

