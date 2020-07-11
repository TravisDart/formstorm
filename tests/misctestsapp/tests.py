from django.test import TestCase
from formstorm import FormTest, FormElement
from .forms import NameForm, BookForm


class NameFormTest(FormTest):
    form = NameForm
    your_name = FormElement(
        good=["or The Whale", "", None],
        bad=["A"*101],
        is_unique=True
    )


class BookFormTest(FormTest):
    form = BookForm
    title = FormElement(
        bad=["A"*101],
        is_unique=True
    )


class BadFormTest(FormTest):
    """
        Make sure an error is thrown when we expect a bad value to be valid.
    """
    form = BookForm
    title = FormElement(
        good=["A"*101],
    )


class NameTestCase(TestCase):
    def setUp(self):
        self.theNameFormTest = NameFormTest()

    def test_name_form(self):
        with self.assertRaises(RuntimeError) as context:
            self.theNameFormTest.run()

        expected_message = 'Uniqueness tests can only be run on ModelForms'
        assert str(context.exception) == expected_message


class BookTestCase(TestCase):
    def setUp(self):
        self.theBookFormTest = BookFormTest()

    def test_book_form(self):
        with self.assertRaises(RuntimeError) as context:
            self.theBookFormTest.run()

        expected_message = 'Good input must be given to run uniqueness test.'
        assert str(context.exception) == expected_message


class BadTestCase(TestCase):
    def setUp(self):
        self.theBadFormTest = BadFormTest()

    def test_book_form(self):
        with self.assertRaises(AssertionError):
            self.theBadFormTest.run()
