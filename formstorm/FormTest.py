import itertools
from .FormElement import FormElement
from django.db import transaction
from django.forms import ModelForm
from .iterhelpers import dict_combo


class FormTest(object):
    is_e2e = False

    def is_good(self):
        return self.bound_form.is_valid()

    def submit_form(self, form_values):
        self.bound_form = self.form(form_values)
        if self._is_modelform and self.bound_form.is_valid():
            self.bound_form.save()

    def _build_elements(self, fields_to_ignore=[]):
        elements = {}
        unique_elements = []
        for e in dir(self):
            if e in fields_to_ignore:
                continue

            # Filter out this class's FormElement properties
            form_element = getattr(self, e)
            if type(form_element) is FormElement:
                elements[e] = form_element.build_iterator(
                    is_e2e=self.is_e2e,
                    form=self.form,
                    field_name=e
                )

                if form_element.is_unique:
                    unique_elements.append(e)

        return elements, unique_elements

    def __init__(self):
        self._is_modelform = ModelForm in self.form.mro()

        # elements is a dictonary of field names, each conaining a list. e.g:
        # elements = {
        #     "title": [  # This is implemented as an iterator, not a list.
        #         ('Moby Dick', True),
        #         (None, False),
        #         ('', False),
        #         ('AA...A', False)
        #     ],
        #     "subtitle": [  # Ditto; see note above.
        #         ('or The Whale', True),
        #         ('', True),
        #         (None, True),
        #         ('AA...A', False)
        #     ]
        # }
        elements, self.unique_elements = self._build_elements()

        # Build iterable from the iterables of the sub-objects. For example:
        # self._iterator = [
        # {'subtitle': ('or The Whale', True), 'title': ('Moby Dick', True) },
        # {'subtitle': ('or The Whale', True), 'title': (None, False)       },
        # {'subtitle': ('or The Whale', True), 'title': ('', False)         },
        # {'subtitle': ('or The Whale', True), 'title': ('AA...A', False)   },
        # {'subtitle': ('', True),             'title': ('Moby Dick', True) },
        # {'subtitle': ('', True),             'title': (None, False)       },
        # {'subtitle': ('', True),             'title': ('', False)         },
        # {'subtitle': ('', True),             'title': ('AA...A', False)   },
        # {'subtitle': (None, True),           'title': ('Moby Dick', True) },
        # {'subtitle': (None, True),           'title': (None, False)       },
        # {'subtitle': (None, True),           'title': ('', False)         },
        # {'subtitle': (None, True),           'title': ('AA...A', False)   },
        # {'subtitle': ('AA...A', False),      'title': ('Moby Dick', True) },
        # {'subtitle': ('AA...A', False),      'title': (None, False)       },
        # {'subtitle': ('AA...A', False),      'title': ('', False)         },
        # {'subtitle': ('AA...A', False),      'title': ('AA...A', False)   }
        # ]
        self._iterator = dict_combo(elements)
        # Generate test values for multi-field validation:
        for v in getattr(self, "additional_values", {}):
            # The easiest way to explain the v2 operation is by example:
            # v = ({"one": 1, "two": 2}, True)
            # v2 = {"one": (1, True), "two": (2, True)}
            v2 = dict(zip(v[0].keys(), [(y, v[1]) for y in v[0].values()]))
            # Build all the combinations of the other fields.
            new_elements = self._build_elements(
                fields_to_ignore=v[0].keys()
            )[0]  # Just take the elements and discard the unique_elements.
            # Combine the values with the element from additional_values.
            addl_iterator = dict_combo(new_elements, base_dict=v2)
            self._iterator = itertools.chain(self._iterator, addl_iterator)

    def run(self):
        # To run uniqueness tests, the form must be a modelform,
        # and at least some good values must be specified.
        # Don't run if there aren't any unique_elements.
        should_run_uniqueness_test = True if self.unique_elements else False
        has_run_uniqueness_test = False if self.unique_elements else True

        if should_run_uniqueness_test and not self._is_modelform:
            raise RuntimeError(
                "Uniqueness tests can only be run on ModelForms"
            )

        # i is a dictionary containing tuples in the form (value, is_good)
        for i in self._iterator:
            # if any field is invalid, the form is invalid.
            form_is_good = all([x[1][1] for x in i.items()])

            # Remove None values from dict.
            form_values = {k: v[0] for k, v in i.items() if v[0] is not None}

            if self._is_modelform:
                sid = transaction.savepoint()

            self.submit_form(form_values)

            if self.is_good() != form_is_good:
                # print("form_values", form_values)
                # print("errors", self.bound_form.errors)
                raise AssertionError

            if self._is_modelform:
                if not has_run_uniqueness_test and form_is_good:
                    # There's no way to verify that the uniqueness constraint
                    # was the one that triggered the error. However, if the
                    # form was previously valid, and now it's not, and we've
                    # submitted the same input, then we can conclude that
                    # non-uniqueness was the issue.
                    self.submit_form(form_values)
                    assert not self.is_good()
                    # Normally, we only test for valid/invalid, but let's
                    # do a little extra and verify which fields caused errors.
                    for field in self.unique_elements:
                        assert self.bound_form.has_error(field)
                    has_run_uniqueness_test = True

                transaction.savepoint_rollback(sid)

        if should_run_uniqueness_test and not has_run_uniqueness_test:
            # If we make it to the end without having run the uniqueness test,
            # then it must be because no good input was specified.
            raise RuntimeError(
                "Good input must be given to run uniqueness test."
            )
