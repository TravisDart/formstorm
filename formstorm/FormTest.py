from FormElement import FormElement
from itertools import chain
from django.db import transaction
from django.forms import ModelForm
from iterhelpers import dict_combo
from functools import reduce


class FormTest(object):
	is_e2e = False


	def is_good(self):
		return self.bound_form.is_valid()


	def submit_form(self, form_values):
		self.bound_form = self.form(form_values)
		if self._is_modelform and self.bound_form.is_good():
			self.bound_form.save()

	
	def __init__(self):
		# Build iterable from the iterables of the sub-objects
		self.elements = {
			key:getattr(self, key).iterator
			for key in dir(self)
			if type(getattr(self, key)) == FormElement
		}
		self._iterator = dict_combo(self.elements)
		self._is_modelform = type(self.form) == ModelForm


	def run(self):
		for is_uniqueness_test in set([False, self._is_modelform]):
			for i in self._iterator:
				# i is a dictionary whose elements are tuples
				# in the form (value, is_good)
				
				# if any field is invalid, the form is invalid.
				form_is_good = reduce(
					lambda x, y: x[1][1] and y[1][1],
					i.items()
				)
				form_values = {
					k:v[0]
					for k, v in i.items()
				}

				sid = transaction.savepoint()

				self.submit_form(form_values)
				print "{},{},{}".format(form_values["title"], form_values["subtitle"], form_is_good) 
				assert self.is_good() == form_is_good

				if is_uniqueness_test:
					transaction.savepoint_commit(sid)
				else:
					transaction.savepoint_rollback(sid)
