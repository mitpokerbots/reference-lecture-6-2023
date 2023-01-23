import random


'''
Key Variables:
Indices to access options in strategy list
regretSum: A list to keep track of the total regret of each decision
strategy: A list to hold the weightings of each option in a mixed strategy
strategySum: The sum of all the strategies used thus far
oppStrategy: The strategy of a theoretical opponent against whom we must adjust

'''



##Returns the adjusted strategy after an iteration
def getStrategy(regretSum,strategySum):
    actions = 3 #3 potential action to RPS
    normalizingSum = 0
    strategy = [0,0,0]
    #Normalizingsum is the sum of positive regrets. 
    #This ensures do not 'over-adjust' and converge to equilibrium
    for i in range(0,actions):
        if regretSum[i] > 0:
            strategy[i] = regretSum[i]
        else:
            strategy[i] = 0
        normalizingSum += strategy[i]
    ##This loop normalizes our updated strategy
    for i in range(0,actions):
        if normalizingSum > 0:
            strategy[i] = strategy[i]/normalizingSum
        else:
            #Default to 33%
            strategy[i] = 1.0 / actions
        strategySum[i] += strategy[i]
    return (strategy,strategySum)


#Returns a random action according to the strategy
def getAction(strategy):
    r = random.uniform(0,1)
    if r >= 0 and r < strategy[0]:
        return 0
    elif r >= strategy[0] and r < strategy[0] + strategy[1]:
        return 1
    elif r >= strategy[0] + strategy[1] and r < sum(strategy):
        return 2
    else:
        return 0


def train(iterations,regretSum,oppStrategy):
    actionUtility = [0,0,0]
    strategySum = [0,0,0]
    actions = 3
    for i in range(0,iterations):
        ##Retrieve Actions
        t = getStrategy(regretSum,strategySum)
        strategy = t[0]
        strategySum = t[1]
        #print(strategy)
        myaction = getAction(strategy)
        #Define an arbitrary opponent strategy from which to adjust
        otherAction = getAction(oppStrategy)   
        #Opponent Chooses scissors
        if otherAction == actions - 1:
            #Utility(Rock) = 1
            actionUtility[0] = 1
            #Utility(Paper) = -1
            actionUtility[1] = -1
        #Opponent Chooses Rock
        elif otherAction == 0:
            #Utility(Scissors) = -1
            actionUtility[actions - 1] = -1
            #Utility(Paper) = 1
            actionUtility[1] = 1
        #Opopnent Chooses Paper
        else:
            #Utility(Rock) = -1
            actionUtility[0] = -1
            #Utility(Scissors) = 1
            actionUtility[2] = 1
            
        #Add the regrets from this decision
        for i in range(0,actions):
            regretSum[i] += actionUtility[i] - actionUtility[myaction]
    return strategySum


def getAverageStrategy(iterations,oppStrategy):
    actions = 3
    strategySum = train(iterations,[0,0,0],oppStrategy)
    avgStrategy = [0,0,0]
    normalizingSum = 0
    for i in range(0,actions):
        normalizingSum += strategySum[i]
    for i in range(0,actions):
        if normalizingSum > 0:
            avgStrategy[i] = strategySum[i] / normalizingSum
        else:
            avgStrategy[i] = 1.0 / actions
    return avgStrategy


oppStrat = [.4,.3,.3]
print("Opponent's Strategy",oppStrat)
print("Maximally Exploitative Strat", getAverageStrategy(1000000,oppStrat))