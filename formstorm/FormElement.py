from itertools import chain
from django.db.models import Q


class FormElement(object):
    def __init__(self,
                 good=[],
                 bad=[],
                 values=[],
                 only_if=[],
                 not_if=[],
                 unique=False,
                 fk_field=None):
        self.bad = bad
        self.good = good
        self.values = values
        self.only_if = only_if
        self.not_if = not_if

    def build_iterator(self, ref_model, is_e2e):
        for i, g in enumerate(self.good):
            if type(g) is Q:
                ref_object = ref_model.objects.get(g)
                if is_e2e:  # If we're doing an e2e test, reference by name.
                    self.good[i] = unicode(ref_object)
                else:
                    self.good[i] = ref_object.pk

        self.iterator = chain(
            [(x, True) for x in self.good],
            [(x, False) for x in self.bad],
            # self.values
        )

        return self.iterator
