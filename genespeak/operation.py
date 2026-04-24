from .util import *

class Operation:
	'''
		An object that carries out behavioral processes as a function of energy / time.
	'''
	def __init__(self, head, data):
		self.head = head
		self.data = data
	def __repr__(self): 
		return f'Operator(id=\'{self.head}\', size={len(self.data)})'
	def convert(tree): return convert(tree)


def convert(tree: list)-> Operation:
	''' 
		Converts a nested parse-tree into a functional operation.
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
