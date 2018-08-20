from FormElement import FormElement
from django.db import transaction
from django.forms import ModelForm
from iterhelpers import dict_combo


class FormTest(object):
    is_e2e = False

    def is_good(self):
        return self.bound_form.is_valid()

    def submit_form(self, form_values):
        self.bound_form = self.form(form_values)
        if self._is_modelform and self.bound_form.is_valid():
            print "Save!"
            self.bound_form.save()

    def _build_elements(self):
        self.elements = {}
        for e in dir(self):
            # Filter out this class's FormElement properties
            if type(getattr(self, e)) is FormElement:
                # If this field is a fk/m2m, get the model that it points to.
                try:
                    ref_model = self.form._meta.model._meta.get_field(e).rel.to
                except AttributeError:
                    ref_model = None

                self.elements[e] = getattr(self, e).build_iterator(
                    is_e2e=self.is_e2e,
                    ref_model=ref_model
                )
                getattr(self, e)

    def __init__(self):
        self._is_modelform = ModelForm in self.form.mro()
        self._build_elements()
        # Build iterable from the iterables of the sub-objects
        self._iterator = dict_combo(self.elements)

    def _run(self, is_uniqueness_test=False):
        # i is a dictionary whose elements are tuples
        # in the form (value, is_good)
        for i in self._iterator:
            # if any field is invalid, the form is invalid.
            form_is_good = all([x[1][1] for x in i.items()])
            form_values = {k: v[0] for k, v in i.items()}

            if self._is_modelform and not is_uniqueness_test:
                sid = transaction.savepoint()

            self.submit_form(form_values)
            assert self.is_good() == form_is_good
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
