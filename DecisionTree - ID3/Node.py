class Node():

	def __init__(self):
		self.values = {}
		self.attr = ""
		self.isLeaf = False
		self.amount = 0
		self.answer = ""			
	def setAttr(self, name):
		self.attr = name

	def setLeaf(self, b):
		self.isLeaf = b

	def setAnswer(self, answer):
		self.answer = answer

	def addAmount(self):
		self.amount += 1

	def setAmount(self, a):
		self.amount = a

	def addChild(self, name, node):
		# print "addin child -------"
		# print self.attr 
		# print self.values
		self.values[name] = node
		# print self.values
		# print "--------------------"