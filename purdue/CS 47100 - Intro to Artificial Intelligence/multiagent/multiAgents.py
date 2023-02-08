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
        
        sumScore = 9999999
        ghostDist = 0
        
        # less dist better score
        
        if (len(newFood.asList()) == len(currentGameState.getFood().asList())):
            for food in newFood.asList():
                sumScore = min(sumScore, manhattanDistance(food, newPos))
        else:
            sumScore = 0
        
        # more dist better score
        for ghost in newGhostStates:
            if (manhattanDistance(ghost.getPosition(), newPos) == 0):
                return -99999999
            ghostDist += (manhattanDistance(ghost.getPosition(), newPos))
        
        "*** YOUR CODE HERE ***"
        return (-1 * 4 * sumScore) + 3 * ghostDist

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    
    def maxAction (self, gameState, depth):
        if (depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), Directions.STOP
        # Multiple min layers, one for each ghost, for every max layer
        # Pacman -> Ghosts
        maxAction = [-999999, ]
        
        pacmanActions = gameState.getLegalActions(self.index)
        for action in pacmanActions:
            # First Ghost for every Max
            newGameState = gameState.generateSuccessor(self.index, action)
            newAction = self.minAction(newGameState, depth, 1)
            if (maxAction[0] < newAction[0]):
                maxAction = [newAction[0], action]
        return maxAction
    
    def minAction (self, gameState, depth, agentIndex):
        if (depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), Directions.STOP
        # For each Ghost, add layers
        # Ghosts -> each Ghost indices
        minAction = [999999, ]
        numGhosts = gameState.getNumAgents()
        pacmanActions = gameState.getLegalActions(agentIndex)
        for action in pacmanActions:
            newGameState = gameState.generateSuccessor(agentIndex, action)
            if (agentIndex + 1 < numGhosts):
                newAction = self.minAction(newGameState, depth, agentIndex + 1)
            else:
                # if this agent is the last ghost, recall max
                newAction = self.maxAction(newGameState, depth - 1)
            if (minAction[0] > newAction[0]):
                minAction = [newAction[0], action]
        return minAction
    
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
        
        # {NORTH, SOUTH, WEST, EAST, STOP}
        "*** YOUR CODE HERE ***"
        action = self.maxAction(gameState, self.depth)
        return action[1]
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxAction (self, gameState, depth, alpha, beta):
        if (depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), Directions.STOP
        # Multiple min layers, one for each ghost, for every max layer
        # Pacman -> Ghosts
        maxAction = [-999999, ]
        
        pacmanActions = gameState.getLegalActions(self.index)
        for action in pacmanActions:
            # First Ghost for every Max
            newGameState = gameState.generateSuccessor(self.index, action)
            newAction = self.minAction(newGameState, depth, 1, alpha, beta)
            
            if (maxAction[0] < newAction[0]):
                maxAction = [newAction[0], action]
                
            if (maxAction[0] > beta):
                return maxAction
            
            alpha = max(alpha, maxAction[0])
        return maxAction
    
    def minAction (self, gameState, depth, agentIndex, alpha, beta):
        if (depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), Directions.STOP
        # For each Ghost, add layers
        # Ghosts -> each Ghost indices
        minAction = [999999, ]
        numGhosts = gameState.getNumAgents()
        pacmanActions = gameState.getLegalActions(agentIndex)
        for action in pacmanActions:
            newGameState = gameState.generateSuccessor(agentIndex, action)
            if (agentIndex + 1 < numGhosts):
                newAction = self.minAction(newGameState, depth, agentIndex + 1, alpha, beta)
            else:
                # if this agent is the last ghost, recall max
                newAction = self.maxAction(newGameState, depth - 1, alpha, beta)
            if (minAction[0] > newAction[0]):
                minAction = [newAction[0], action]
                
            if (minAction[0] < alpha):
                return minAction
            
            beta = min(beta, minAction[0])
        return minAction
    
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action = self.maxAction(gameState, self.depth, -9999999, 9999999)
        return action[1]
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def maxAction (self, gameState, depth):
        if (depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), Directions.STOP
        # Multiple min layers, one for each ghost, for every max layer
        # Pacman -> Ghosts
        maxAction = [-999999, ]
        
        pacmanActions = gameState.getLegalActions(self.index)
        for action in pacmanActions:
            # First Ghost for every Max
            newGameState = gameState.generateSuccessor(self.index, action)
            newAction = self.uniformAction(newGameState, depth, 1)
            if (maxAction[0] < newAction[0]):
                maxAction = [newAction[0], action]
        return maxAction
    
    def uniformAction (self, gameState, depth, agentIndex):
        if (depth == 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), Directions.STOP
        # For each Ghost, add layers
        # Ghosts -> each Ghost indices
        total = 0
        numGhosts = gameState.getNumAgents()
        pacmanActions = gameState.getLegalActions(agentIndex)
        for action in pacmanActions:
            newGameState = gameState.generateSuccessor(agentIndex, action)
            if (agentIndex + 1 < numGhosts):
                newAction = self.uniformAction(newGameState, depth, agentIndex + 1)
            else:
                # if this agent is the last ghost, recall max
                newAction = self.maxAction(newGameState, depth - 1)
            total += newAction[0]
        return total / len(pacmanActions), Directions.STOP
    
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        action = self.maxAction(gameState, self.depth)
        return action[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
        Negative foodScore because closer value is more prioritized
        Positive ghostDist because further ghost is more prioritized
        Ratio: currentScore >>>> foodScore > ghostDist
        So score is added up with very large number of curScore + foodScore + ghostDist
    """
    "*** YOUR CODE HERE ***"
    
    myPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    
    foodScore = 9999999
    ghostDist = 9999999
    
    # less dist better score
    
    for food in foodPos:
        foodScore = min(foodScore, manhattanDistance(food, myPos))
    # more dist better score
    for ghost in ghostStates:
        if (manhattanDistance(ghost.getPosition(), myPos) == 0):
            return -99999999
        ghostDist = min(ghostDist, manhattanDistance(ghost.getPosition(), myPos))
    
    score = (-4 * foodScore) + 3 * ghostDist
    score += 100000 * currentGameState.getScore()
    return score

# Abbreviation
better = betterEvaluationFunction
