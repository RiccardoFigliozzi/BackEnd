from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.template.loader import render_to_string
# Create your views here.

months_dict = {
    'january': 'Eccolo!',
    'february': 'Eccolo!',
    'march': 'Eccolo!',
    'april': 'Eccolo!',
    'may': 'Eccolo!',
    'june': 'Eccolo!',
    'july': 'Eccolo!',
    'august': 'Eccolo!',
    'september': 'Eccolo!',
    'october': 'Eccolo!',
    'november': 'Eccolo!',
    'december': 'Eccolo!'
}

def index(request):
    list_items=''
    month_list=list(months_dict.keys())
    response_data = render(request, 'challenges/index.html', {
        'month_index': month_list,
    })
    return response_data

def monthly_challenge(request, month):
    try:
        challenge_text = months_dict[month]
        return render(request, 'challenges/challenge.html',
                      {'challenge_text': challenge_text,
                       'month' : month})
    except:
        raise Http404()
    
def monthly_challenge_by_number(request,month_number):
    try:
        months_list= list(months_dict.keys())
        redirect_month=months_list[month_number-1]
        reverse_path= reverse('month-challenge', args=[redirect_month])
        return HttpResponseRedirect(reverse_path)
    except:
        raise Http404()