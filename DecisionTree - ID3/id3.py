from Node import Node
import math
import csv
import sys


def pruning(node):
	prune = True

	children = node.values.values()

	for c in children:
		if not c.isLeaf:
			if not pruning(c):
				prune = False

	maxAmount = 0
	maxLabel = ""
	if prune:
		for c in children:
			if c.amount > maxAmount:
				maxAmount = c.amount
				maxLabel = c.answer

		node.setLeaf(True)
		node.setAnswer(maxLabel)
		node.setAmount(maxAmount)
		return True

def predictMany(tree, attrs, data):
	answers = []
	for d in data:
		answers.append(predict(tree, attrs, d))
	return answers

def calculateAccuracy(pred, labels):
	hits = 0.0
	
	for p,l in zip(pred, labels):
		if p == l:
			hits +=1.0

	return hits / len(pred)

def predict(tree, attrs, entry):

	if tree.isLeaf:
		return tree.answer
	# attr = tree.attr
	# i = attrs.index(attr)
	return predict(tree.values[entry[attrs.index(tree.attr)]], attrs, entry)



def getValues(data, attributes, attr):
	index = attributes.index(attr)
	values = []
	for entry in data:
		if entry[index] not in values:
			values.append(entry[index])
	return values

def entropy(data, attr, target):

	entropy = 0.0
	frequency = {}
	index = attr.index(target)
	values = getValues(data, attr, target)

	for d in data:
		if frequency.has_key(d[index]):
			frequency[d[index]] += 1.0
		else:
			frequency[d[index]] = 1.0

	for f in values:
		entropy += (-frequency[f]/len(data)) * math.log(frequency[f]/len(data), 2) 

	return entropy

def gain(data, attr, target, wantedAttr):

	gain = entropy(data,attr,target)
	
	index = attr.index(wantedAttr)

	values = getValues(data, attr, wantedAttr)
	
	sumAll = 0.0

	for v in values:
		
		# reducedData = getData(data, attr, wantedAttr, v)
		nV = 0.0
		for d in data:
			if d[index] == v:
				nV += 1.0

		p = nV / len(data)

		newData = [entry for entry in data if entry[index] == v]
		p *= entropy(newData, attr, target)

		sumAll += p

	gain -= sumAll

	return gain

def findBestAttr(data, attr, target):
	nGain = []

	nAttr = attr[:]
	nAttr.remove(target)
	for a in nAttr:
		nGain.append(gain(data, attr, target, a))

	index = nGain.index(max(nGain))

	return attr[index]

def getData(data, attr, best, v):
	nData = []
	# print best
	# print v
	index = attr.index(best)

	for d in data:
		# amostra corresponde a classe buscadas
		if d[index] == v:
			#cria copia temporaria da amostra
			tmp = []
			# copia todos valores menos o valor do atributo buscado
			for t in d:
				if (t != v):
					tmp.append(t)
			nData.append(tmp)
	return nData

def majority(data, attr, target):
	index = attr.index(target)

	freq = {}

	for d in data:
		if freq.has_key(d[index]):
			freq[d[index]] += 1
		else:
			freq[d[index]] = 1

	major = max(freq.values())

	for v in freq.keys():
		if freq[v] == major:
			return v

def id3(data, attr, target):
	# print "New run"
	n = Node()
	# print "Beginning "
	# print n.values
	ans = getValues(data, attr, target)
	
	# Ha somente 1 classificacao possivel para estes dados
	if len(ans) == 1:
		n.setLeaf(True)
		n.setAnswer(ans[0])
		i = attr.index(target)
		for d in data:
			if d[i] == ans[0]:
				n.addAmount()
		# print "Leaf Created"
		return n

	# Se nao ha atributos restantes
	if (len(attr) - 1) <= 0:
		n.isLeaf(True)
		answer = majority(data,attr,target)
		n.setAnswer(answer)
		for d in data:
			if d[i] == answer:
				n.addAmount()
		# print "Leaf Created"
		return n

	best = findBestAttr(data, attr, target)
	# print "Best: " + best

	# Remove o atributo que sera o novo nodo da arvore
	nAttr = attr[:]
	nAttr.remove(best)

	values = getValues(data, attr, best)
	# print values
	for v in values:
		# print v
		nData = getData(data, attr, best, v)

		if len(nData) <= 0:
			n.isLeaf(True)
			n.setAnswer(majority(data,attr,target))
			for d in data:
				if d[i] == answer:
					n.addAmount()
			# print "Leaf Created"
			return n

		n.setAttr(best)
		# nNode = id3(nData, nAttr, target)
		n.addChild(v,id3(nData, nAttr, target))

	return n

def read_csv(filename) :
	attributes = []
	examples = []

	with open(filename, "r") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

		firstline = True

		for row in spamreader:
			if firstline:
				for item in row:
					attributes.append(item)

				firstline = False
			else:
				examples.append(row)

	return (attributes, examples)

def main():
	attr, data = read_csv(sys.argv[1])
	target = attr[-1]

	# print entropy(data, attr, target)
	# print gain(data, attr, target, "Outlook")
	# print findBestAttr(data, attr, target)
	# print majority(data, attr, target)

	n = id3(data,attr,target)

	# pruning(n)
	# print n.attr
	# print n.values
	printTree(n, "")

	answers = predictMany(n, attr, data)
	for a in answers:
		print a
	print calculateAccuracy(answers, [d[-1] for d in data])
	# print predict(n, attr, ["Overcast", "Mild", "High", "Strong"])
	# print predict(n, attr, ["Overcast", "Hot", "Normal", "Weak"])
	# print predict(n, attr, ["Rain", "Mild", "High", "Strong"])

def printTree(n, espace):

	if n.isLeaf:
		print espace + n.answer + " " + str(n.amount)
	else:
		for v in n.values:
			print espace + n.attr + " == " + v
			printTree(n.values[v], espace + "\t\t")

if __name__ == '__main__':
	main()