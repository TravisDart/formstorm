from django.test import TestCase
from formstorm import FormTest, FormElement
from .forms import NameForm, BookForm


class BadNameFormTest(FormTest):
    form = NameForm
    your_name = FormElement(
        good=["Ishmael"],
        bad=["A"*101, "", None],
        is_unique=True
    )


class NameFormTest(FormTest):
    form = NameForm
    your_name = FormElement(
        good=["Ishmael"],
        bad=["A"*101, "", None],
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


class BadNameTestCase(TestCase):
    def setUp(self):
        self.theBadNameFormTest = BadNameFormTest()

    def test_name_form(self):
        with self.assertRaises(RuntimeError) as context:
            self.theBadNameFormTest.run()

        expected_message = 'Uniqueness tests can only be run on ModelForms'
        assert str(context.exception) == expected_message


class NameTestCase(TestCase):
    def setUp(self):
        self.theNameFormTest = NameFormTest()

    def test_book_form(self):
        self.theNameFormTest.run()


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
