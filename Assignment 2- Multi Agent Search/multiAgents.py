# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newGhostPositions = successorGameState.getGhostPositions() # get positions of all the ghosts
        maximizers = []
        minimizers = []

        #calculate pacman's distance to nearest ghost + 1
        ghostDistances = []
        for ghostPos in newGhostPositions:
            distance = util.manhattanDistance(ghostPos, newPos)
            ghostDistances.append(distance)
        minGhostDist = min(ghostDistances) + 1
        
        #calculate pacman's distance to nearest food pellet
        foodList = newFood.asList() #first get a list of all the foods
        foodDistances = []
        for food in foodList:
            distance = util.manhattanDistance(food, newPos)
            foodDistances.append(distance)
        if not foodDistances: minFoodDist = 1 # if food distance is empty, use 1
        else: minFoodDist = min(foodDistances)
        
        scaredTimes = sum(newScaredTimes) # sum the scared time for each scared ghost

        # add all the maximizers
        maximizers.append(successorGameState.getScore()) # the higher the score, the better
        maximizers.append(1.0 / minFoodDist) # the closer a food, the better
        maximizers.append(1.0/(1.0+len(newFood.asList()))) # the more food eaten, the better
        
        # if pacman is invincible, minGhostDist is a maximizer
        # otherwise, it is a minimizer
        if newScaredTimes and newScaredTimes[0]:
            maximizers.append(1.0/minGhostDist)
            maximizers.append(scaredTimes) # this will only be nonzero if pacman is invincible
        else:
            minimizers.append(1.0/minGhostDist)
            
        # calculate the result
        result = sum(maximizers)
        if minimizers: result -= sum(minimizers)
        
        return result
        

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.pacmanIndex = 0
        self.initialDepth = 0
        self.alpha = -999999999
        self.beta = 999999999

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        result = self.maxOrMin(gameState, self.initialDepth, self.pacmanIndex, True)
        moveToReturn = result[0]
        return moveToReturn

    def getValue(self, gameState, depth, agent, isMax):
    
        # if the state is a terminal state: return the state's utility
        testDepth = gameState.getNumAgents() * self.depth 
        if gameState.isLose() or gameState.isWin() or (depth == testDepth):
            return self.evaluationFunction(gameState)
            
        # if the next agent is MAX: return max-value(state)
        if agent == 0:
            isMax = True
            
        # if the next agent is MIN: return min-value(state)
        else:
            isMax = False
            
        result = self.maxOrMin(gameState, depth, agent, isMax)
            
        return result[1]

    def maxOrMin(self, gameState, depth, agent, isMax):
    
        # initialize v
        if isMax: val = -999999999  
        else: val = 999999999
        
        # get all legal actions for this agent
        actions = gameState.getLegalActions(agent)
        
        # get each successor of state
        successors = [("", val)]
        successors = self.getSuccessors(gameState, depth, agent, actions, successors, isMax)
            
        # sort successors, according to second value in tuples
        if isMax:
            successors.sort(reverse = True, key = lambda x: x[1]) # descending order
        else:
            successors.sort(key = lambda x: x[1]) # ascending order
        
        return successors[0] # return ideal successor and it's directional step
        
    def getSuccessors(self, gameState, depth, agent, actions, successors, isMax):
        for a in actions:
            successorState = gameState.generateSuccessor(agent, a)
            successorDepth = depth + 1
            successorAgent = successorDepth % gameState.getNumAgents()
            successor = self.getValue(successorState, successorDepth, successorAgent, isMax)
            successors.append((a, successor))
        return successors        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        result = self.maxOrMin(gameState, self.initialDepth, self.pacmanIndex, True, self.alpha, self.beta)
        moveToReturn = result[0]
        return moveToReturn

    def getValue(self, gameState, depth, agent, isMax, alpha, beta):
    
        # if the state is a terminal state: return the state's utility
        testDepth = gameState.getNumAgents() * self.depth 
        if gameState.isLose() or gameState.isWin() or (depth == testDepth):
            return self.evaluationFunction(gameState)
            
        # if the next agent is MAX: return max-value(state)
        if agent == 0:
            isMax = True
            
        # if the next agent is MIN: return min-value(state)
        else:
            isMax = False
            
        result = self.maxOrMin(gameState, depth, agent, isMax, alpha, beta)
        return result[1]

    def maxOrMin(self, gameState, depth, agent, isMax, alpha, beta):
        
        # initialize v
        if isMax: val = -999999999  
        else: val = 999999999
        act = "Stop"
        
        # get all legal actions for this agent
        actions = gameState.getLegalActions(agent)
        
        # get each successor of state
        for a in actions:
            successorState = gameState.generateSuccessor(agent, a)
            successorDepth = depth + 1
            successorAgent = successorDepth % gameState.getNumAgents()
            successor = self.getValue(successorState, successorDepth, successorAgent, isMax, alpha, beta)
            
            # if we're handing max value operation
            if isMax:
                if val < successor:
                    val = successor
                    act = a
                # prune
                if val > beta: 
                    return act, val
                else: alpha = max(val, alpha)
                
            # we're handling a min value operation
            else:
                if val > successor:
                    val = successor
                    act = a
                # prune
                if val < alpha:
                    return act, val
                else: beta = min(val, beta)
                
        return act, val # return ideal successor and it's directional step
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        result = self.maxOrMin(gameState, self.initialDepth, self.pacmanIndex, True)
        moveToReturn = result[0]
        return moveToReturn

    def getValue(self, gameState, depth, agent, isMax):
    
        # if the state is a terminal state: return the state's utility
        testDepth = gameState.getNumAgents() * self.depth 
        if gameState.isLose() or gameState.isWin() or (depth == testDepth):
            return self.evaluationFunction(gameState)
            
        # if the next agent is MAX: return max-value(state)
        if agent == 0:
            isMax = True
            
        # if the next agent is MIN: return min-value(state)
        else:
            isMax = False
            
        result = self.maxOrMin(gameState, depth, agent, isMax)
        return result[1]

    def maxOrMin(self, gameState, depth, agent, isMax):
    
        # initialize v
        if isMax: val = -999999999  
        else: val = 999999999
        
        # get all legal actions for this agent
        actions = gameState.getLegalActions(agent)
        
        # get each successor of state
        successors = [("", val)]
        successors = self.getSuccessors(gameState, depth, agent, actions, successors, isMax)
            
        # sort successors, if we're getting max
        if isMax:
            successors.sort(reverse = True, key = lambda x: x[1]) # descending order
            return successors[0]
            
        # Return expectimax sum with dummy direction
        else:
            return "West", sum(s[1] for s in successors)
        
    def getSuccessors(self, gameState, depth, agent, actions, successors, isMax):
        val = 0
        for a in actions:
            successorState = gameState.generateSuccessor(agent, a)
            successorDepth = depth + 1
            successorAgent = successorDepth % gameState.getNumAgents()
            successor = self.getValue(successorState, successorDepth, successorAgent, isMax)
            val = successor / len(actions)
            if isMax: successors.append((a, successor))
            else: successors.append((a, val))
        return successors  
        
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This Evaluation function takes into account the following...
        Maximizers:
            - Current game score
            - Minimum ghost distance (if ghosts are scared)
            - Sum of all the scared ghost timers (if ghosts are scared)
            - Distance to nearest food pellet
            - Remaining uneaten food
            - Average food distance
            - Random integer (if positive)
        Minimizers:
            - Minimum ghost distance (if not scared and in close range)
            - Random integer (if negative)
            
    """
    "*** YOUR CODE HERE ***"
    # Sentinel values if game is end state
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
  
    # get variables to use in calculations
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhostPositions = currentGameState.getGhostPositions() # get positions of all the ghosts
    numFood = currentGameState.getNumFood()
    score = currentGameState.getScore()
    if score == 0: score += 1
    
    maximizers = []
    minimizers = []
        
    #calculate pacman's distance to nearest ghost + 1
    ghostDistances = []
    for ghostPos in newGhostPositions:
        distance = util.manhattanDistance(ghostPos, newPos)
        ghostDistances.append(distance)
        if distance < 2: 
            return -float('inf')
    minGhostDist = min(ghostDistances) + 1
        
    # calculate pacman's distance to each food pellet
    foodList = newFood.asList() #first get a list of all the foods
    foodDistances = []
    for food in foodList:
        distance = util.manhattanDistance(food, newPos)
        foodDistances.append(distance)
        
    # get the minimum food distance
    if not foodDistances: minFoodDist = 1 # if food distance is empty, use 1
    else: minFoodDist = min(foodDistances)
    
    # get the average food distance
    avgFoodDist = sum(foodDistances) / len(foodDistances)
    if avgFoodDist == 0: avgFoodDist = 1 # avoid division by zero
        
    # invincible pacman should benefit him, so take the sum of times of scared ghosts
    scaredTimes = sum(newScaredTimes) 
    randomNum = random.randrange(-1, 2, 1)
    
    # add all the maximizers
    maximizers.append(score) # the higher the score, the better
    maximizers.append(2.0 / minFoodDist) # the closer a food, the better
    maximizers.append(2.0 / numFood) # inverse of uneaten foods
    maximizers.append(1.0 / avgFoodDist)
    maximizers.append(randomNum) # this random number is to avoid pacman paralyzation 
        
    # if pacman is invincible, minGhostDist is a maximizer
    # otherwise, it is a minimizer
    if newScaredTimes and newScaredTimes[0]:
        maximizers.append(20.00/minGhostDist)
        maximizers.append(scaredTimes) # this will only be nonzero if pacman is invincible
    else:
        ghostDistanceVal = 2.0/minGhostDist
        if ghostDistanceVal >= 4: # if the ghost is really far, this shouldn't factor in
            minimizers.append(2.0/minGhostDist)
            
    # calculate the result
    result = sum(maximizers)
    if minimizers: result -= sum(minimizers)
    
    return result

# Abbreviation
better = betterEvaluationFunction
