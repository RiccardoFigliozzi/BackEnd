from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ReviewForm
from .models import Review

# Create your views here.

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = Review(user_name=form.cleaned_data['user_name'],
                            review_text=form.cleaned_data['review_text'],
                            rating=form.cleaned_data['rating'])
            review.save()
            res = HttpResponseRedirect('/thank-you')
            return res
    else:
        form = ReviewForm()

    res = render(request, 'reviews/review.html', {"form":form})
    return res

def thank_you(request):
    res = render(request, 'reviews/thank_you.html')
    return res