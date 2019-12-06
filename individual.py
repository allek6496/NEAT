from math import e
from random import uniform
import numpy as np

'''
The static structure has the following inputs and outputs
Inputs:
	Your balls
	Enemy's balls
	Your ducks
	Enemy's ducks
	Your points
	Enemy's points
	Your previous move
	Enemy previous move
	Enemy second previous move
	Enemy third previous move
	Enemy fourth previous move
	Enemy fifth previous move
	Enemy sixth previous move
	Enemy seventh previous move
	Enemy eighth previous move
	Enemy ninth previous move
	And a bias node that is always 1
Outputs:
	Three numbers, [0, 1, 2]
	0 is throw
	1 is duck
	2 is reload
	The biggest of the three numbers is used, unless it's impossible, in which case the second biggest and so on. If it tries to do something impossible, big hit to the preformance
'''
class individual:
	def __init__(self, genome=None):
		self.maxMutation = 0.1 #Max amount a weight can be changed by
		self.largePopulation = 15 #What constitutes a large species
		self.maxRandom = 3 #How random the totally random mutation is

		self.genome = []
		self.nodes = ["i"]*17 + ["o"]*3 #The list of nodes and their types

		for gene in genome:
			self.genome += gene

	def getAction(self, inputs):
		text = {0: "throw", 1: "duck", 2: "reload"}

		outputs = [self.getNode(10, inputs), 
				   self.getNode(11, inputs), 
				   self.getNode(12, inputs)]
		decisions = []

		for i in range(3):
			decision = outputs.index(max(outputs))
			outputs.pop(decision)
			decisions.append(text, text.pop(decision))

		return decisions

	#Activation function, maps from -inf -> +inf to 0 -> 1
	@staticmethod
	def activate(sum):
		return 1/(1+e**(-4.9*sum))

	#Recursive function that finds the value of a node
	def getNode(self, node, inputs):
		sum = 0
		for gene in self.genome:
			if gene[1] == node and gene[3] == 1:
				if self.nodes[gene[0]] != 'i':
					sum += self.getNode(gene[0], inputs)*gene[2]
				else:
					sum += inputs[gene[0]]*gene[2]
		return self.activate(sum)

	def mutateWeights(self):
		for gene in self.genome:
			if uniform(0, 1) < 0.8:
				if uniform(0, 1) < 0.9:
					gene[2] += uniform (-1, 1)*self.maxMutation
				else:
					gene[2] = uniform(-1, 1)*self.maxRandom
			
	def mutateStructure(self, popSize, previousNum):
		if uniform(0, 1) < 0.03:
			self.nodes += ['h']
			self.genome += []
			pass
		elif popSize >= self.largePopulation and uniform(0, 1) < 0.3:
			#add link with random weight
			pass
		elif uniform(0, 1) < 0.05:
			#add link with random weight
			pass
		else:
			return previousNum
		
		return previousNum + 1
