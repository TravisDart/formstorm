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
        for e in dir(self):
            if e in fields_to_ignore:
                continue

            # Filter out this class's FormElement properties
            if type(getattr(self, e)) is FormElement:
                elements[e] = getattr(self, e).build_iterator(
                    is_e2e=self.is_e2e,
                    form=self.form,
                    field_name=e
                )

        return elements

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
        elements = self._build_elements()

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
            new_elements = self._build_elements(fields_to_ignore=v[0].keys())
            # Combine the values with the element from additional_values.
            addl_iterator = dict_combo(new_elements, base_dict=v2)
            self._iterator = itertools.chain(self._iterator, addl_iterator)

    def _run(self, is_uniqueness_test=False):
        # i is a dictionary containing tuples in the form (value, is_good)
        for i in self._iterator:
            # if any field is invalid, the form is invalid.
            form_is_good = all([x[1][1] for x in i.items()])

            # Remove None values from dict.
            form_values = {k: v[0] for k, v in i.items() if v[0] is not None}

            if self._is_modelform and not is_uniqueness_test:
                sid = transaction.savepoint()

            self.submit_form(form_values)

            if self.is_good() != form_is_good:
                # print("form_values", form_values)
                # print("errors", self.bound_form.errors)
                raise AssertionError

            if is_uniqueness_test and form_is_good:
                self.submit_form(form_values)
                assert not self.is_good()

            if self._is_modelform and not is_uniqueness_test:
                transaction.savepoint_rollback(sid)

    def run(self):
        self._run(is_uniqueness_test=False)
        # self._run(is_uniqueness_test=True)

    def run_uniqueness_tests(self):
        pass

    def run_individual_tests(self):
        self._run(is_uniqueness_test=False)
