from formstorm import FormTest, FormElement
from formstorm.iterhelpers import every_combo
from .forms import BookForm
from django.test import TestCase
from .models import Author, Genre
from django.db.models import Q


class BookFormTest(FormTest):
    form = BookForm
    title = FormElement(
        good=["Moby Dick"],
        bad=[None, '', "A"*101],
    )
    subtitle = FormElement(
        good=[None, "", "or The Whale"],
        bad=["A"*101]
    )
    author = FormElement(
        good=[Q(name="Herman Melville")],
        bad=[None, "", -1]
    )
    is_fiction = FormElement(
        good=[True, False],
        bad=[None, "", -1, "A"]
    )
    pages = FormElement(
        good=[0, 10, 100],
        bad=[None, "", "A"]
    )
    genre = FormElement(
        good=every_combo([
            Q(name="Mystery"),
            Q(name="History"),
            Q(name="Humor")
        ]),
        bad=[None]
    )


class BookTestCase(TestCase):
    def setUp(self):
        Genre(name="Mystery").save()
        Genre(name="History").save()
        Genre(name="Humor").save()
        Author(name="Herman Melville").save()
        Author(name="Charles Dickens").save()
        self.theBookFormTest = BookFormTest()

    def test_book_form(self):
        self.theBookFormTest.run()
