from django.forms import ModelForm
from minimalapp.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = []
