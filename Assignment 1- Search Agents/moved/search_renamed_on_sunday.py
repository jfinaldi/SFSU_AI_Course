# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    # copy the start position of pacman
    curState = problem.getStartState()
    print("curState: ", curState)

    # initialize the frontier as a stack
    frontier = util.Stack()
    successors = problem.getSuccessors(curState)
    for successor in successors:
        frontier.push((successor[0], [successor[1]]))

    # initialize an empty list of explored steps
    explored = []
    explored.append(curState)

    # Start Loop to traverse deepest nodes first
    while 1:
    
        # if frontier is empty return failure
        if frontier.isEmpty(): 
            print("(111)frontier is empty. Returning failure...")
            return []

        # if frontier is not empty, traverse the graph
        else:
            # take a node off the frontier and reassign current state to new state
            nextStep, direction = frontier.pop()
            curState = nextStep

            # check for goal state, if so, return all of the N,S,E,W directions that
            # got us there
            if problem.isGoalState(curState):
                return direction
                
            # otherwise, expand the next node and add its children to frontier
            if not curState in explored: 
                explored.append(curState)
                allSuccessors = problem.getSuccessors(curState)
                for successor in allSuccessors:
                    frontier.push((successor[0], direction + [successor[1]]))
        
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    # copy the start position of pacman
    curState = problem.getStartState()
    #print("curState: ", curState)

    # initialize the frontier as a stack
    frontier = util.Queue()
    successors = problem.getSuccessors(curState)
    for successor in successors:
        frontier.push((successor[0], [successor[1]]))

    # initialize an empty list of explored steps
    explored = []
    explored.append(curState)

    # Start Loop to traverse shallowest nodes first
    while 1:
    
        # if frontier is empty return failure
        if frontier.isEmpty():  
            print("(156)frontier is empty. Returning failure...")
            return [] 
        
        # if frontier is not empty, traverse the graph 
        else:
            # take a node off the frontier and reassign current state to new state    
            nextStep, direction = frontier.pop()
            curState = nextStep
            
            # check for goal state, if so, return all of the N,S,E,W directions that
            # got us there
            if problem.isGoalState(curState):
                return direction
            
            # otherwise, expand the next node and add its children to frontier
            if not curState in explored: 
                explored.append(curState)
                allSuccessors = problem.getSuccessors(curState)
                for successor in allSuccessors:
                    frontier.push((successor[0], direction + [successor[1]]))
    
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    # copy the start position of pacman
    curState = problem.getStartState()
    print("curState: ", curState)

    # initialize the frontier as a stack
    frontier = util.PriorityQueue()
    successors = problem.getSuccessors(curState)
    for successor in successors:
        frontier.update((successor[0], [successor[1]], successor[2]), successor[2])

    # initialize an empty list of explored steps
    explored = []
    explored.append(curState)

    # Start Loop to traverse cheapest nodes first
    while 1:
    
        # if frontier is empty return failure
        if frontier.isEmpty():  
            print("(202)frontier is empty. Returning failure...")
            return [] 
        
        # if frontier is not empty, traverse the graph 
        else:
            # take a node off the frontier and reassign current state to new state    
            nextStep, direction, _ = frontier.pop()
            curState = nextStep
            
            # check for goal state, if so, return all of the N,S,E,W directions that
            # got us there
            if problem.isGoalState(curState):
                return direction
            
            # otherwise, expand the next node and add its children to frontier
            if not curState in explored: 
                explored.append(curState)
                allSuccessors = problem.getSuccessors(curState)
                for successor in allSuccessors:
                    route = direction + [successor[1]]
                    cost = problem.getCostOfActions(route)
                    frontier.update((successor[0], route, successor[2]), cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    # copy the start position of pacman
    curState = problem.getStartState()
    
    # initialize the frontier as a stack
    frontier = util.PriorityQueue()
    frontier.update((curState, [], 0), 0)
    
    # initialize an empty dictionary of explored steps
    explored = {curState: 0}
    
    # Start Loop to traverse cheapest nodes first
    while 1:
    
        # if frontier is empty return failure
        if frontier.isEmpty():  
            #print("[251]frontier is empty. Returning failure...")
            result = []
            print("result: ", result)
            return result
        
        # if frontier is not empty, traverse the graph 
        else:
            # take a node off the frontier and reassign current state to new state    
            (nextStep, direction, cost) = (frontier.pop())
            
            # check for goal state, if so, return all of the N,S,E,W directions that
            # got us there
            if problem.isGoalState(nextStep):
                print("A* returning path: ", direction)
                return direction
            
            # otherwise, expand the next node and add its children to frontier
            allSuccessors = problem.getSuccessors(nextStep)
            for successor in allSuccessors:
                
                #calculate all the costs for this successor
                route = direction + [successor[1]]
                gCost = problem.getCostOfActions(route)
                hCost = heuristic(successor[0], problem)
                fCost = gCost + hCost
                
                # if the fCost is lower than any state matches in explored, reassign
                # or if state isn't already in explored, then put it there 
                aSuccessor = successor[0]
                if len(aSuccessor) > 1:
                    #print("aSuccessor is a tuple with list")
                    aSuccessor = aSuccessor[0]
                #print("aSuccessor: ", aSuccessor)
                if explored.get(aSuccessor) is None or fCost < explored[aSuccessor]:
                    explored[aSuccessor] = fCost
                    frontier.update((successor[0], route, gCost), fCost)

            
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
