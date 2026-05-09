from .util import LANGUAGE, set_language
from .operation import Operation
import string

def get_definition(op: str)-> str:
	"""
		Returns the definition of a symbol.
	"""
	if op in LANGUAGE.operators: return LANGUAGE.operators[op]
	elif op in LANGUAGE.setters: return LANGUAGE.setters[op]
	elif op in LANGUAGE.constructs: return LANGUAGE.constructs[op]
	elif op in LANGUAGE.regulators: return LANGUAGE.regulators[op]


def get_type(obj, context: dict={}):
	"""
		Returns the type of an object in a given context.
	"""
	if isinstance(obj, Operation):
		return get_definition(obj.head)['dtype']
	else:
		if isinstance(obj, str):
			if obj in context:
				return get_type(context[obj], context)
		else:
			for i in LANGUAGE.dtypes:
				if isinstance(obj, tuple(LANGUAGE.dtypes[i])):
					return i


def define(type, id, name=None, arity=None, dtype=None, input=None, function=None):
	data = {}
	data['id'] = id
	data['name'] = name
	data['arity'] = arity
	data['dtype'] = dtype
	data['input'] = input
	data['function'] = function
	LANGUAGE.insert(type, data)


def convert(tree: list)-> Operation:
	tree = list(tree)
	''' 
		Converts a parse tree into an operation.
	'''
	if isinstance(tree, list):
		if len(tree) > 0:
			head = tree[0]
			data = tree[1:]
			for i in range(len(data)):
				x = data[i]
				if isinstance(x, list):
					data[i] = convert(x)
			return Operation(head, data)


def validate(operation: Operation, context: dict)-> bool:
	'''
		Checks the validity of an operation in a given context.
	'''
	if isinstance(operation, list): operation = convert(operation)

	definition = get_definition(operation.head)

	if definition is not None:
		arity = definition['arity']

		if arity is not None:
			if isinstance(arity, list):
				low,high = arity
			else: low,high = arity,arity

			if not (low is None or len(operation.data) >= low):
				raise Warning("Too few parameters")
				return False
			if not (high is None or len(operation.data) <= high):
				raise Warning("Too many parameters")
				return False

			if 'input' in definition:
				input = definition['input']

				if input is not None:
					if not isinstance(input, list):
						input = [input] * len(operation.data)

					for i in range(len(input)):
						x = operation.data[i]
						if isinstance(x, str) and x in context:
							x = context[x]

						if isinstance(input[i], str):
							if get_type(x) != input[i]:
								raise Warning("Invalid parameter type")
								return False
						return True
		return True

	# raise Warning("Invalid symbol")
	return False


def execute(operation: Operation, context: dict):
	'''
		Executes an operation in a given context.
	'''
	if isinstance(operation, list): 
		operation = convert(operation)

	op = operation.head	
	if op in LANGUAGE.operators or op in LANGUAGE.setters:
		inputs = []
		for i in range(len(operation.data)):
			child = operation.data[i]
			if op not in LANGUAGE.setters or i > 0:
				if isinstance(child, Operation):
					child = execute(child, context)
				elif isinstance(child, str):
					if child.isnumeric():
						if child.isdecimal():
							child = float(child)
						else: child = int(child)
					else: child = context[child]
			inputs.append(child)

		if op in LANGUAGE.setters:
			func = LANGUAGE.setters[op]['function']
			return func(context, *inputs)
		else: 
			func = LANGUAGE.operators[op]['function']
			return func(inputs)

	elif op in LANGUAGE.constructs:
		construct = LANGUAGE.constructs[op]

		if construct['name'] == 'rule':
			condition, action = operation.data
			if execute(condition, context):
				execute(action, context)
				return True
			return False

		elif construct['name'] == 'list':
			for action in operation.data:
				execute(action, context)
			return True

	elif op in LANGUAGE.regulators:
		regulator = LANGUAGE.regulators[op]
		inputs = []
		for i in range(len(operation.data)):
			child = operation.data[i]
			if isinstance(child, (list, tuple)):
				child = execute(child, context)
	
			if isinstance(child, str):
				if child.isnumeric():
					if child.isdecimal():
						child = float(child)
					else: child = int(child)
				else: child = context[child]
			inputs.append(child)
		return Operation(operation.head, inputs)
	else:
		inputs = []
		for i in range(len(operation.data)):
			child = operation.data[i]
			if isinstance(child, (list, tuple)):
				child = execute(child, context)
	
			if isinstance(child, str):
				if child.isnumeric():
					if child.isdecimal():
						child = float(child)
					else: child = int(child)
				else: child = context[child]
			inputs.append(child)
		return Operation(operation.head, inputs)


