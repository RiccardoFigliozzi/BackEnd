from django import forms

class ReviewForm(forms.Form):
    user_name = forms.CharField(label='Your name', max_length=200, error_messages={
        "required": "Must not be empty",
        "max_length": "Not empty or more than 200 characters"
    })

    review_text = forms.CharField(label='Your Feedback', widget=forms.Textarea, max_length=200)
    rating = forms.IntegerField(label='Your Rating', min_value=1, max_value=5)