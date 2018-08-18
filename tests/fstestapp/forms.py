from django.forms import ModelForm
from .models import Author, Book


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        exclude = []


class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = []
