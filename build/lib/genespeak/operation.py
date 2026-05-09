from .util import LANGUAGE

class Operation:
	'''
		An object that carries out behavioral processes as a function of energy / time.
	'''
	def __init__(self, head, data):
		super().__init__()
		self.head = head
		self.data = data

	def __repr__(self):
		s = '' + str(self.head)
		if len(self.data) > 0:
		  s += LANGUAGE.terminals['sep']
		for i in range(len(self.data)):
			s += str(self.data[i])
			if i < len(self.data)-1:
				s += LANGUAGE.terminals['sep']
		s = LANGUAGE.terminals['open'] + s + LANGUAGE.terminals['close']
		return s 