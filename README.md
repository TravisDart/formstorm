# FormStorm (v1.0.0)

FormStorm is a Python library that easily creates unit tests for Django forms by defining valid/invalid values for each field. All combinations of the fields' predefined values are submitted to the form to validate each field and test for unintended interdependence between fields. In addition to testing single- and multi-field validation, FormStorm can also test single-field uniqueness constraints by double-submitting a valid submission and checking which fields become invalid on the 2nd submission.

## Example:

Suppose we have a form to create a Book object. The book's name is mandatory,
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

Validating multi-field constraints can be tested by specifying the values (as a dictionary) along with the expected results. For example, if the "title" and "subtitle" fields can't have a combined length greater than 150 characters, we can test this constraint like so:

    additional_values = [
        ({'title': "A"*100, 'subtitle': "A"*50}, True),
        ({'title': "A"*50, 'subtitle': "A"*100}, True),
        ({'title': "A"*100, 'subtitle': "A"*51}, False),
        ({'title': "A"*51, 'subtitle': "A"*100}, False),
    ]

## Install:

    pip install formstorm

## TODO:


- End-to-end testing (with Selenium): This is partially implemented, and most of the necessary FormStorm functions have been abstracted. Just need to subclass FormTest and fully implement.
- Tests for DRF Serializers. "SerializerStorm"
- Set up CI
- Handle the obscure, "long tail" cases by implementing a framework to define tests for any type of constraint (such as multi-column uniqueness constraints). To do this, a "sub-test" would define one or more form submissions and the (boolean) result expected. Sub-tests would be combined with each other and with the standard combinatorial mix of good/bad values so that all fields are tested simultaneously. A tentative definition of the sub-tests is below:


    sub_tests = [
        { # Sub-test 1
            field_names=["field1","field2",..."fieldN"],
            submissions = [ Each sub-test consists of multilpe submissions.
                (  # Submission 1 
                    value1,  # the value for field1
                    value2,  # the value for field2
                    ...
                    valueN,  # the value for fieldN
                    result,  # the expected result of the submission
                ),
                (...), # Submission 2
                ...
                (...)  # Submission N
            ]
        },
        {...}, # Sub-test 2
        ...
        {...}  # Sub-test N
    ]

For example, suppose a model has two fields that have a multi-column uniqueness constraint:

    class SomeModel(models.Model):
        field1 = models.TextField()
        field2 = models.TextField()
        field3 = models.TextField()
        ...
        fieldN = models.TextField()

        class Meta:
            constraints = [
                UniqueConstraint(
                    fields=['field1', 'field2'], name='unique_together'
                )
            ] 

The sub-test to test this constraint would be defined like this:

    class SomeModelFormTest(FormTest):
    	form = SomeModelForm
        sub_tests = [
            {
                field_names=["field1","field2"],
                submissions = [
                    ("a","a", True),
                    ("a","b", True),  # Duplicate values in one column are fine
                    ("b","a", True),  # ... as are duplicates in the other column
                    ("a","a", False)  # ... but the same values again should fail
                ]
            }
        ]
        field3 = FormElement(good=[...], bad=[...])
        ...
        fieldN = FormElement(good=[...], bad=[...])

The advantage of this is that we can define a test only for the fields affected by a constraint, and have values for the other fields supplied by the normal good/bad value tests.
