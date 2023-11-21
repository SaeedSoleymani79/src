from django import forms
from .models import User_Bookmark, Rate, Comment, Books

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rate']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['review']


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = User_Bookmark
        fields = ['reading_status', 'reading_progress']
