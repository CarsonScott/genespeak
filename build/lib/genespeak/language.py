from functools import reduce
import json

class Language:
	terminals: dict = {}
	dtypes: dict = {}
	operators: dict = {}
	setters: dict = {}
	constructs: dict = {}

	def copy(self, other):
		self.dtypes = other.dtypes
		self.operators = other.operators
		self.setters = other.setters
		self.constructs = other.constructs
		self.terminals = other.terminals
		return self

	def load(filename):
		lang = Language()
		f = open(filename, 'r')
		data = json.load(f)

		dtypes = data['dtypes']
		terminals = data['terminals']
		setters = data['setters']
		operators = data['operators']
		constructs = data['constructs']

		for i in dtypes:
			if not isinstance(dtypes[i], list):
				dtypes[i] = [dtypes[i]]
			for j in range(len(dtypes[i])):
				dtypes[i][j] = eval(dtypes[i][j])

		lang.dtypes = dtypes
		lang.terminals = terminals

		for operator in operators:
			id = operator['id']
			f = operator['function']
			operator['function'] = eval(f"lambda x: reduce({f}, x)")
			lang.operators[id] = operator

		for setter in setters:
			id = setter['id']
			f = eval(setter['function'])
			setter['function'] = f
			lang.setters[id] = setter

		for construct in constructs:
			id = construct['id']
			lang.constructs[id] = construct

		return lang
