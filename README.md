# FormStorm (v1.0.0)

A library to test Django forms by trying (almost) every combination of valid and invalid input. Rather than testing each field's validation independently, formstorm tests all of the fields' validation simultaneously to ensure that there is no interdependence between fields.

Note that Version 1 only verifies that there is no interdependence between fields. The next version will be able to test forms that have multi-field and interdependent validation.

## Example:

Suppose we have a form to create a book object. The book's name is mandatory,
but the subtitle is optional. A `FormTest` is created that provides examples 
of valid and invalid values for each field:


    from django.forms import ModelForm
    from formstorm import FormTest, FormElement
    from django.test import TestCase
    
    
    class Book(models.Model):
        title = models.CharField(max_length=100, blank=False, null=False)
        subtitle = models.CharField(max_length=100, blank=True, default="")
    
    
    class BookForm(ModelForm):
        class Meta:
            model = Book
            exclude = []
    
    
    class BookFormTest(FormTest):
    	form = BookForm
    	title = FormElement(
    		good = ["Moby Dick"],
    		bad = [None, "", "A"*101],
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


When the `FormTest` runs, the form will be tested with every combination of 
each field's possible values. Namely, the form will be tested with these values:


|  title    | subtitle     | result  | 
|-----------|--------------|---------| 
| Moby Dick | ""           | Valid   | 
| Moby Dick | None         | Valid   | 
| None      | None         | Invalid | 
| ""        | None         | Invalid | 
| AA[...]AA | None         | Invalid | 
| None      | ""           | Invalid | 
| ""        | ""           | Invalid | 
| AA[...]AA | ""           | Invalid | 
| Moby Dick | or The Whale | Valid   | 
| None      | or The Whale | Invalid | 
| ""        | or The Whale | Invalid | 
| AA[...]AA | or The Whale | Invalid | 
| Moby Dick | AA[...]AA    | Invalid | 
| None      | AA[...]AA    | Invalid | 
| ""        | AA[...]AA    | Invalid | 
| AA[...]AA | AA[...]AA    | Invalid | 

Without something like FormStorm, you either have to tediously create test cases
for each possible input value, or you have to just trust that the form behaves
how you intend it to.

(A runnable implementation of the example above can be found in [tests/minimalapp/](tests/minimalapp/).)

## Advanced Example:

An example showing how to use different field types can be found in [tests/fstestapp/test.py](tests/fstestapp/test.py).

Basically, all fields work as above, with the exception of ForeignKey and Many2Many fields whose values must be specified with `Q()` objects. Also, example values for multi-valued fields (such as Many2Many) can be created with the `every_combo()` function which returns every combination of the Many2Many options.

To test the validation of multiple fields, 

    additional_values = [
        ({'title': "A"*100, 'subtitle': "A"*50}, True),
        ({'title': "A"*50, 'subtitle': "A"*100}, True),
        ({'title': "A"*100, 'subtitle': "A"*51}, False),
        ({'title': "A"*51, 'subtitle': "A"*100}, False),
    ]

## Install:

    pip install formstorm

## TODO:

- Test to ensure that uniqueness constraints work. - Some provision for this feature has already been made, but it hasn't been fully implemented yet. 
- End-to-end testing (with Selenium): This is partially implemented, and all of the necessary FormStorm functions have been abstracted. Just need to subclass FormTest and fully implement.
- Tests for DRF Serializers. "SerializerStorm"
- Set up CI
