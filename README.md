# FormStorm (v1.0.0 beta1)

A library to test Django forms by trying (almost) every combination of valid and invalid input. - Sort of like a brute-force attack on your form.

## Example:

Suppose we have a form to create a book object. The book's name is mandatory,
but the subtitle is optional. A `FormTest` is created that provides examples 
of valid and invalid values for each field:


    from django.forms import ModelForm
    from formstorm import FormTest, FormElement
    from django.test import TestCase
    
    
    class Book(models.Model):
        title = models.CharField(max_length=100, blank=False, null=False)
        subtitle = models.CharField(max_length=100)
    
    
    class BookForm(ModelForm):
        class Meta:
            model = Book
            exclude = []
    
    
    class BookFormTest(FormTest):
    	form = BookForm
    	title = FormElement(
    		good = ["Moby Dick"],
    		bad = [None, '', 'A'*101],
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
| Moby Dick | None         | Valid   | 
| None      | None         | Invalid | 
| ""        | None         | Invalid | 
| AA[...]AA | None         | Invalid | 
| Moby Dick | ""           | Valid   | 
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

## Advanced example:

An example showing how to use different field types can be found in [tests/fstestapp/test.py](tests/fstestapp/test.py).

Basically, all fields work as above, with the exception of ForeignKey and Many2Many fields whose values must be specified with `Q()` objects. Also, example values for multi-valued fields (such as Many2Many) can be created with the `every_combo()` function which returns every combination of the Many2Many options.

## Install:

    pip install formstorm

## TODO:

- Test to ensure that uniqueness constraints work. - Some provision for this feature has already been made, but it hasn't been fully implemented yet. 
- End-to-end testing (with Selenium): This is partially implemented, and all of the necessary FormStorm functions have been abstracted. Just need to subclass FormTest and fully implement.
- Tests for DRF Serializers. "SerializerStorm"
- Set up CI
- Support for dynamic values that depend on other values: For instance, suppose a Contact form either collects a company name or an individual name, depending on the contact type. We wouldn't want to supply a value for `individual_name` if it's not a company, so we'd need to implement like so:


        class Contact(models.Model):
            is_company = models.BooleanField(default=False)
            company_name = models.CharField(max_length=100, blank=True, null=True)
            individual_name = models.CharField(max_length=100, blank=True, null=True)
        
            def clean():
                if self.is_company and not self.company_name:
                    raise ValidationError("Please specify a company name.")
                elif not self.is_company and not self.individual_name:
                    raise ValidationError("Please provide your first and last name.")
        
        
        class ContactFormTest(FormTest):
            form = ContactForm
            is_company = FormElement(good = [True, False], bad=[None])
            company_name = FormElement(
                good=["Acme, Inc."],
                bad=[None],
                only_if=["is_company"]
            )
            individual_name = FormElement(
                good=["John Doe"],
                bad=[None],
                not_if=["is_company"]
            )

- Rather than specifying good/bad values, give the option to pass an iterator that returns (value, is_good).

        class AuthorFormTest(FormTest):
            form = AuthorForm
            name = FormElement(
                values=ValueHelper(values_iterator, depends_on=["field1","field2"])
                good=[...],
                bad=[...]
            )
- Support for [faker functions](https://github.com/joke2k/faker), using ValueHelper, as above. This would test the form with 3 names generated by fake.name():
        
        from faker import Faker
        fake = Faker()
        
        class AuthorFormTest(FormTest):
            form = AuthorForm
            name = FormElement(
                good=[
                    "Herman Melville",
                    "Charles Dickens",
                    ValueHelper(fake.name, cardinality=3, is_good=True)
                ],
            )
