from formstorm import FormTest, FormElement
from forms import AuthorForm, BookForm
from django.test import TestCase


class BookFormTest(FormTest):
	form = BookForm
	title = FormElement(
		good = ["Moby Dick"],
		bad = [None, '', "A"*101],
	)
	subtitle = FormElement(
		good = [None, "", "or The Whale"],
		bad = ["A"*101]
	)


class BookTestCase(TestCase):
    def setUp(self):
        self.theBookFormTest = BookFormTest()

    def test_book_form(self):
        self.theBookFormTest.run()
