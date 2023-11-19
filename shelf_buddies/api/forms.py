from django import forms
from .models import Rate, Comment
class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rate']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['review']