from django.test import TestCase
from formstorm import FormTest, FormElement
from .forms import BookForm


class BookFormTest(FormTest):
    form = BookForm
    title = FormElement(
            good=["Moby Dick"],
            bad=[None, "", "A"*101],
    )
    subtitle = FormElement(
            good=["or The Whale", "", None],
            bad=["A"*101]
    )


class BookTestCase(TestCase):
    def setUp(self):
        self.theBookFormTest = BookFormTest()

    def test_book_form(self):
        self.theBookFormTest.run()
