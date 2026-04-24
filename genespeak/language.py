from functools import reduce
import json

class Language:
	dtypes: dict = {}
	operators: dict = {}
	setters: dict = {}
	constructs: dict = {}
	terminals: dict = {}

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
		context = data['context']
		setters = data['setters']
		operators = data['operators']
		constructs = data['constructs']

		locals = {}

		statement = "\n".join(context)
		exec(statement, locals=locals)

		for i in dtypes:
			if not isinstance(dtypes[i], list):
				dtypes[i] = [dtypes[i]]
			for j in range(len(dtypes[i])):
				dtypes[i][j] = eval(dtypes[i][j], locals=locals)

		lang.dtypes = dtypes
		lang.terminals = terminals

		for operator in operators:
			id = operator['id']
			f = operator['function']
			f = eval(f"lambda x: reduce({f}, x)", locals=locals)
			operator['function'] = f
			lang.operators[id] = operator

		for setter in setters:
			id = setter['id']
			f = eval(setter['function'], locals=locals)
			setter['function'] = f
			lang.setters[id] = setter

		for construct in constructs:
			id = construct['id']
			lang.constructs[id] = construct

		return lang
