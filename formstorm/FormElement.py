from itertools import chain


class FormElement(object):
	def __init__(self, good=[], bad=[], values=[], only_if=[], not_if=[]):
		self.good = good
		self.bad = bad
		self.values = values
		self.only_if = only_if
		self.not_if = not_if
		self.iterator = chain(
			[(x, True) for x in self.good],
			[(x, False) for x in self.bad],
			# self.values
		)
