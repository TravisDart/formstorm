from itertools import chain
from django.db.models import Q
from six import text_type


class FormElement(object):
    def __init__(self, good=[], bad=[], is_unique=False):
        self.bad = bad
        self.good = good
        self.is_unique = is_unique 

    def build_iterator(self, form, field_name, is_e2e):
        """
        Suppose in a Book model, Book.genre is a foreign key to a Genre model,
        and in the Book test we have:

        genre = FormElement(
            good=[Q(name="Mystery")],
        )

        If good=[Q(name="Mystery")] then replace good with the pk of the
        Mystery object. Essentially (although this is not the algorithm used)
        the object is replaced with:
        good = [ Genre.objects.get(name="Mystery").pk ]
        """
        def _get_pk_for_q(q_object):
            # 1st: Find the model that the field points to.
            form_field = form._meta.model._meta.get_field(field_name)
            try:  # Python 3
                ref_model = form_field.remote_field.model
            except AttributeError:
                ref_model = form_field.rel.to

            # 2nd: Get the object that the Q object points to.
            ref_object = ref_model.objects.get(q_object)

            # 3rd: Get the identifier for that object.
            if is_e2e:  # If we're doing an e2e test, reference by name.
                return text_type(ref_object)
            else:
                return ref_object.pk

        def _replace_all_q(value_list):
            for i, g in enumerate(value_list):
                if type(g) is Q:
                    value_list[i] = _get_pk_for_q(g)
                elif type(g) in [list, tuple]:
                    value_list[i] = [
                        _get_pk_for_q(j)
                        if type(j) is Q else j
                        for j in g
                    ]
            return value_list

        self.good = _replace_all_q(self.good)
        self.bad = _replace_all_q(self.bad)
        self.iterator = chain(
            [(x, True) for x in self.good],
            [(x, False) for x in self.bad],
        )
        return self.iterator
