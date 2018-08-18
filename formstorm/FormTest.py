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


	def submit_form(self, form_params):
		self.bound_form = self.form(form_params)
		print "self.bound_form", self.bound_form
		print "self.bound_form", self.bound_form.errors()
		print "self.bound_form", self.bound_form.is_valid()
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


	@transaction.atomic
	def _do_step(self, form_params, should_rollback=True):
		self.submit_form(form_params)
		if should_rollback:
			transaction.rollback()


	def run(self):
		for is_modelform in set([False, self._is_modelform]):
			for i in self._iterator:
				# i is a dictionary whose elements are tuples
				# in the form (value, is_good)
				should_be_good = reduce(
					lambda x, y: x[1][1] and y[1][1],
					i.items()
				)
				form_values = {
					k:v[0]
					for k, v in i.items()
				}

				self.submit_form(form_params=i)
				print i, self.is_good(), should_be_good
				assert self.is_good() == should_be_good
