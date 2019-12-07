from math import e
from random import uniform, choice
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
		self.maxMutation = 0.1 #max amount a weight can be changed by
		self.largePopulation = 15 #what constitutes a large species
		self.maxRandom = 3 #how random the totally random weight is

		self.genome = []
		self.nodes = ["i"]*17 + ["o"]*3 #the list of nodes and their types

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

	#activation function, maps from -inf -> +inf to 0 -> 1
	@staticmethod
	def activate(sum):
		return 1/(1+e**(-4.9*sum))

	#recursive function that finds the value of a node
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
		#80% chance to be changed
		if uniform(0, 1) < 0.8:

			#go through each gene
			for gene in self.genome:

				#90% to change by a small amount
				if uniform(0, 1) < 0.9:
					gene[2] += uniform (-1, 1)*self.maxMutation
				#10% to be totally different
				else:
					gene[2] = uniform(-1, 1)*self.maxRandom
			
	def mutateStructure(self, popSize, previousNum):
		if uniform(0, 1) < 0.03 and len(self.genome) > 0:
			self.nodes += ['h']

			#pick a random enabled gene to split into two
			gene = choice([g for g in self.genome if g[3] == 1])
			
			#disable this gene
			gene[3] = 0 

			#make a new gene going to the node we just added with weight 1
			self.genome.append([gene[0], len(self.nodes)-1, 1, 1, previousNum + 1])

			#make a gene coming from the new node with the old weight
			self.genome.append([len(self.nodes)-1, gene[1], gene[2], 1, previousNum + 2])
			
			#two numbers were used so increment by two
			return previousNum + 2
			
		elif popSize >= self.largePopulation and uniform(0, 1) < 0.3:
			self.genome.append([])
			
			#pick a random non-output node to come from
			self.genome[-1].append(choice([e.index for e in self.nodes if e != 'o']))

			#pick a random non-input node to go to
			self.genome[-1].append(choice([e.index for e in self.nodes if e != 'i']))

			#add a random weight to this node
			self.genome[-1].append(uniform(-1, 1)*self.maxRandom)

			#set it to be enabled
			self.genome[-1].append(1)

			#give it the new innovation number
			self.genome[-1].append(previousNum + 1)
			return previousNum + 1
		elif uniform(0, 1) < 0.05:
			#same code as in the previous part
			self.genome.append([])
			self.genome[-1].append(choice([e.index for e in self.nodes if e != 'o']))
			self.genome[-1].append(choice([e.index for e in self.nodes if e != 'i']))
			self.genome[-1].append(uniform(-1, 1)*self.maxRandom)
			self.genome[-1].append(1)
			self.genome[-1].append(previousNum + 1)
			return previousNum + 1
		else:
			return previousNum