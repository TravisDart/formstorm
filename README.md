# FormStorm

A library to test forms by trying (almost) every combination of valid and invalid input. - Sort of like a brute-force attack on your form.


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