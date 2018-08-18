from formstorm import FormTest, FormElement
from forms import AuthorForm, BookForm
from django.test import TestCase


class BookFormTest(FormTest):
	form = BookForm
	name = FormElement(
		good = ["Moby Dick"],
		bad = [None, ''],
	)
	sub_title = FormElement(
		good = [None, "", "or The Whale"],
	)


class BookTestCase(TestCase):
    def test_book_form(self):
        theTest = BookFormTest()
        theTest.run()
