from django import forms
from .models import Book

class Book_insert(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'read_states', 'description']

form = Book_insert()

class book_form(forms.Form):
    title       = forms.CharField()
    author      = forms.CharField()
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 20}))
    read_states  =forms.ChoiceField(choices={('read','read'), ('want to read','want to read'), ('reading','reading')}, initial=('want to read'))