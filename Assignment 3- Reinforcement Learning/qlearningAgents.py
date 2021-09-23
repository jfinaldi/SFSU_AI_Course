# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.Q = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        result = self.Q[(state, action)]
        if result: 
            return result
        else:
            return 0.0

        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        Q = [] # initialize empty list of Q values
        
        actions = self.getLegalActions(state) # get legal actions
        if not actions:
            return 0.0 # if no legal actions, return
            
        # loop through all actions
        for a in actions:
            Q.append(self.getQValue(state, a)) # get Q value, store in list
            
        # return max Q value in list
        if len(Q) == 0:
            return 0.0
        else:
            return max(Q)
            
        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = [] # initialize a list of actions
        targetValue = self.computeValueFromQValues(state)
        legalActions = self.getLegalActions(state)
        
        # if no legal actions, return
        if not legalActions:
            return None
        
        # loop through all legal actions
        for a in legalActions:
            q = self.getQValue(state, a)
            
            # add this action to the list if its q value matches the target Q value
            if q == targetValue:
                actions.append(a)
        
        # if our actions list is not empty, return a random action
        if actions:
            return random.choice(actions)
        else:
            return None
              
        
        util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        
        # if no actions, we are at a terminal state, return None
        if not legalActions:
            return action
        
        coin = util.flipCoin(self.epsilon) # flip a coin
        #print("coin: ", coin)
        
        if not coin:
            action = self.getPolicy(state)
        else:
            action = random.choice(legalActions)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        
        """
        Equation needed to implement:
        Q(s, a) = (1 - alpha) Q(s, a) + alpha * [R(s, a, s') + Y max(a')Q(s',a')]
        """
        
        # copy equation component variables
        q = self.Q[(state, action)]
        a = self.alpha
        d = self.discount
        r = reward
        v = self.getValue(nextState)

        # plug into the Q update equation listed above
        self.Q[(state, action)] = ((1 - a) * q) + (a * (r + (d * v)))

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        
        # get the feature vector
        featureVector = self.featExtractor.getFeatures(state, action)
        
        # if empty return default value
        if not featureVector:
            return 0
        
        # obtain weights and return the product of the two 
        w = self.getWeights()
        result = w * featureVector
        return result
        
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        
        # copy component variables
        featureVector = self.featExtractor.getFeatures(state, action)
        a = self.alpha
        d = self.discount
        v = self.getValue(nextState)
        q = self.getQValue(state, action)
        r = reward
        
        # difference = (r + Y*max_a'[Q(s',a')]) - Q(s,a)
        diff = (r + (d * v)) - q 
        
        # for all features in the vector, add the new weight to the current one
        for feature in featureVector:
            f = featureVector[feature]
            w = a * diff * f # wi <- wi + a * difference * fi(s, a)
            self.weights[feature] += w 

        return
            
        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print("weights: ", self.weights)
            pass
