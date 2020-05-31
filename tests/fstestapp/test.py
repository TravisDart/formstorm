from formstorm import FormTest, FormElement
from formstorm.iterhelpers import every_combo, dict_combo
from .forms import BookForm
from django.test import TestCase
from .models import Author, Genre
from django.db.models import Q


class BookFormTest(FormTest):
    form = BookForm
    title = FormElement(
        good=["Moby Dick"],
        bad=[None, "", "A"*101],
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
        good=[True, False, None, "", -1, "A"],
        bad=[]  # Boolean input is either truthy or falsy, so nothing is bad.
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


class UtilTest(TestCase):
    def test_every_combo(self):
        x = every_combo([1, 2, 3])
        assert list(x) == [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]

    def test_dict_combo(self):
        x = dict_combo({
            "a": ["A", "B", "C"],
            "b": [0, 1],
            "c": [True, False, None],
        })

        y = [
            {'a': 'A', 'b': 0, 'c': True},
            {'a': 'A', 'b': 0, 'c': False},
            {'a': 'A', 'b': 0, 'c': None},
            {'a': 'A', 'b': 1, 'c': True},
            {'a': 'A', 'b': 1, 'c': False},
            {'a': 'A', 'b': 1, 'c': None},
            {'a': 'B', 'b': 0, 'c': True},
            {'a': 'B', 'b': 0, 'c': False},
            {'a': 'B', 'b': 0, 'c': None},
            {'a': 'B', 'b': 1, 'c': True},
            {'a': 'B', 'b': 1, 'c': False},
            {'a': 'B', 'b': 1, 'c': None},
            {'a': 'C', 'b': 0, 'c': True},
            {'a': 'C', 'b': 0, 'c': False},
            {'a': 'C', 'b': 0, 'c': None},
            {'a': 'C', 'b': 1, 'c': True},
            {'a': 'C', 'b': 1, 'c': False},
            {'a': 'C', 'b': 1, 'c': None},
        ]

        assert list(x) == y


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
