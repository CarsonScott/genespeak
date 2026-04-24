from .util import *
from .operation import Operation, convert

class Language:
	dtypes: dict = {}
	operators: dict = {}
	setters: dict = {}
	connectors: dict = {}


	def get_type(self, obj, context={}):
		if isinstance(obj, Operation):
			if obj['id'] in self.operators:
				op = self.operators[obj['id']]
				type = op['dtype']
				return type
		else:
			if isinstance(obj, str):
				return self.get_type(context[obj], context)
			else:
				for i in self.dtypes:
					if isinstance(obj, tuple(self.dtypes[i])):
						return i


	def validate(self, operation, context={}):
		if isinstance(operation, list):
			operation = convert(operation)

		head = operation.head
		data = operation.data

		if head in self.operators:
			op = self.operators[head]
			arity = op['arity']

			if arity is not None:
				if isinstance(arity, list): low, high = arity
				else: low, high = arity, arity
				if (low is None or len(data) >= low) and (high is None or len(data) <= high):
					for i in range(len(data)):
						type = self.get_type(data[i], context)
						if type != op['input']:
							return False
					return True
			else: return True
		return False


	def execute(self, operation: Operation, context: dict):
		'''
			Performs an operation on a given input.
		'''
		if isinstance(operation, list): 
			operation = convert(operation)

		op = operation.head

		if op in self.operators or op in self.setters:
			inputs = []
			for i in range(len(operation.data)):
				child = operation.data[i]
				if op not in self.setters or i > 0:
					if isinstance(child, Operation):
						child = self.execute(child, context)
					elif isinstance(child, str):
						if child.isnumeric():
							if child.isdecimal():
								child = float(child)
							else: child = int(child)
						else: child = context[child]
				inputs.append(child)

			if op in self.setters:
				func = self.setters[op]['function']
				return func(context, *inputs)
			else: 
				func = self.operators[op]['function']
				return func(inputs)

		elif op in self.connectors:
			connector = self.connectors[op]

			if connector['name'] == 'rule':
				condition, action = operation.data
				if self.execute(condition, context):
					self.execute(action, context)
					return True
				return False

			elif connector['name'] == 'sequence':
				for action in operation.data:
					self.execute(action, context)
				return True


	def load(filename):
		lang = Language()

		f = open(filename, 'r')
		data = json.load(f)

		dtypes = data['dtypes']
		context = data['context']
		setters = data['setters']
		operators = data['operators']
		connectors = data['connectors']

		locals = {}

		statement = "\n".join(context)
		exec(statement, locals=locals)

		for i in dtypes:
			if not isinstance(dtypes[i], list):
				dtypes[i] = [dtypes[i]]
			for j in range(len(dtypes[i])):
				dtypes[i][j] = eval(dtypes[i][j], locals=locals)

		lang.dtypes = dtypes

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

		for connector in connectors:
			id = connector['id']
			lang.connectors[id] = connector

		return lang
