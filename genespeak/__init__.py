from .util import LANGUAGE, set_language
from .operation import Operation



def translate(op: str)-> str:
	if op in LANGUAGE.operators: return LANGUAGE.operators[op]
	elif op in LANGUAGE.setters: return LANGUAGE.setters[op]
	elif op in LANGUAGE.constructs: return LANGUAGE.constructs[op]



def convert(tree: list)-> Operation:
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


def get_type(operation: Operation, context: dict={}):
	if isinstance(operation, Operation):
		return translate(operation.head)['dtype']
	else:
		if isinstance(obj, str):
			if obj in context:
				return get_type(context[obj], context)
		else:
			for i in self.dtypes:
				if isinstance(obj, tuple(self.dtypes[i])):
					return i


def validate(operation: Operation, context: dict)-> bool:
	'''
		Checks the validity of an operation in a given context.
	'''
	if isinstance(operation, list):
		operation = convert(operation)

	definition = translate(operation.head)

	if definition is not None:
		arity = definition['arity']

		if arity is not None:
			if isinstance(arity, list):
				low,high = arity
			else: low,high = arity,arity

			if not (low is None or len(operation.data) >= low):
				print("Too few parameters")
				return False
			if not (high is None or len(operation.data) <= high):
				print("Too many parameters")
				return False

			if 'input' in definition:
				input = definition['input']

				if input is not None:
					if not isinstance(input, list):
						input = [input] * len(operation.data)

					for i in range(len(input)):
						x = operation.data[i]

						if isinstance(input[i], str): 
							if get_type(x) != input[i]:
								print("Invalid parameter type")
								return False
		return True

	print("Invalid symbol")
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

		elif construct['name'] == 'sequence':
			for action in operation.data:
				execute(action, context)
			return True

'''
Low-Level Constructs:
	expression: (a > b);
	statement:  (a = b + 1);
	production: ((a > b) => (a = b + 1));

Blocks:
	1) Collection - An unordered set of statements that execute concurrently.
	2) Sequence - A set of statements that execute in order until one fails or all of them succeed.
	3) Selector - A set of statements that execute in order until one succeeds or all of them fail.

Collections are sets of objects with no logical structure, meaning they are largely independent of 
one another despite operating within a shared super-structure. The permanence of a given collection
is equivalent to the sum-permanences of its components.

Sequences are used to perform step-by-step tasks. They respond positively only if every step has 
succeeded, meaning they trigger a flux of energy that reinforces their structural wellbeing within
the system. Otherwise, like all genetic constructs, they decay out of existence through diffusion
of matter and energy.

Selectors are different in that they search for a singular valid task in response to a given state.
Whatever task responds first to a given state is selected for execution, effectively halting the 
search for alternatives. The selector thus reinforces itLANGUAGE when a single task becomes active
from its set of possibilities.

Selectors containing all production-rules function exactly like chains of if-then-else statements.
Blocks exists functionally outside the scope of formal language, with dynamics that do not translate
directly to expressions/statements.


* All genetic constructs have a "shelf life" which is dictated by the energy required to maintain 
	the physical structure along with the average rate of "returns" it generates.These are fluxes of 
	energy resulting from the successful execution of a construct to completion. This diffusion of
	energy strengthens active structures and thus reinforces those structures which brought it about.
	This keeps genetic constructs alive that "justify" their own existence by paying off their "debt"
	faster than they can be destroyed. 

	If a construct is unable to generate enough energy to sustain itLANGUAGE over a period of time (or if
	the context in which it is active does not provide enough support), it decays into "precursors", or 
	non-functional physical components, and any amount of energy that
	was used to maintain its structure.


'''
