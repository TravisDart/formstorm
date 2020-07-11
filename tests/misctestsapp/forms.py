from django.forms import ModelForm
from minimalapp.models import Book
from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = []
