from individual import individual

#how simmilar individuals within a species are
dt = 3

#constants used in the difference function
c1, c2, c3 = 1, 1, 0.4

#the difference between two individuals
def delta(indi1, indi2):
    E, D, WSum, WNum = 0, 0, 0, 0
    N = max([20, len(indi1), len(indi2)])
    N = 1 if N == 20 else N
    indi2Genes = [gene2[4] for gene2 in indi2.genome]
    for gene in indi1.genome:
        if gene[4] > indi2.genome[-1][4]: #if this innovation number is greater than the greatest of the other's innovation numbers, then it's excess
            E += 1
        elif gene[4] not in indi2Genes: #if it's not bigger but not in there either, it's disjoint
            D += 1
        else:
            WNum += 1
            WSum += abs(gene[2]-indi1.genome[indi2Genes.index(gene[4])][2])
    return c1*E/N + c2*D/N+c3*WSum/WNum

def game(indi1, indi2):
    f = [0, 0]

    snow1, snow2 = 1, 1
    ducks1, ducks2 = 5, 5
    lives1, lives2 = 3, 3
    history = []
    turns = 0

    while turns < 30 and f == [0, 0]:
        turns += 1

        history1, history2 = [], []
        for j in range(0, 9):
            try:
                history1 += [history[-(j+1)][0]]
            except IndexError:
                history1 += [-1]
            
            try:
                history2 += [history[-(j+1)][1]]
            except IndexError:
                history2 += [-1]

        inputs1 = [snow1, snow2,
                   ducks1, ducks2,
                   lives1, lives2, 
                   history1[0], 
                   *history2]
        
        inputs2 = [snow2, snow1,
                   ducks2, ducks1,
                   lives2, lives1,
                   history2[0], 
                   *history2]

        ch1 = indi1.getAction(inputs1)
        ch2 = indi2.getAction(inputs2)

        history[i] == [ch1, ch2]

        if ch1 == 0:
            if snow1 > 0:
                snow1 -= 1
            else:
                f[0] = -5
        elif ch1 == 1:
            if ducks1 > 0:
                ducks1 -= 1
            else:
                f[0] = -5
        elif ch1 == 2:
            if snow1 < 10:
                snow1 += 1
            else:
                f[0] = -5

        if ch2 == 0:
            if snow2 > 0:
                snow2 -= 1
            else:
                f[1] = -5
        elif ch2 == 1:
            if ducks2 > 0:
                ducks2 = -1
            else:
                f[1] = -5
        elif ch2 == 2:
            if snow2 < 10:
                snow2 += 1
            else:
                f[1] = -5
        
        if ch1 == 0 and ch2 == 2:
            lives2 -= 1
        elif ch2 == 0 and ch1 == 2:
            lives1 -= 1

        if f == [0, 0]:
            if lives1 == 0:
                f[0] = -2
                f[1] = 1
                return f
            elif lives2 == 0:
                f[1] = 1
                f[0] = -2
                return f

    return f

pop = [individual() for i in range(150)] #creates a bunch of blank individuals
fitnesses = [0]*150

global innoNum

for indi in pop:
    for i in range(10):
        innoNum = indi.mutateStructure(150, innoNum)

#store each of the different species
specs = []

for i in range(len(pop)):
    for spec in specs:
        if delta(pop[i], pop[spec[0]]) < dt:
            spec.append(i)
            break
    else:
        specs.append([i])

#runs each individual against another individual and updates their fitness
for i1 in range(len(pop)):
    for i2 in range(i1+1, len(pop)):
        #there is no need to play any two bots more than once because the same thing will happen each time (no randomness)

        results = game(pop[i1], pop[i2])
        fitnesses[i1] += results[0]
        fitnesses[i2] += results[1]
        
#adjusts the fitnesses for the species size
for i in range(len(fitnesses)):
    #search for the species this individual is in
    s = 0
    for spec in specs:
        try:
            s = spec.index(i)
            break
        except IndexError:
            continue
    
    fitnesses[i] = fitnesses[i]/len(specs[s])

#TODO: add crossover and future population creation