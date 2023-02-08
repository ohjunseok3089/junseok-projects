# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        mdp = self.mdp
        
        for i in range(self.iterations):
            state = mdp.getStates()
            values_copy = util.Counter()
            for curState in state:
                value_list = []
                actions = mdp.getPossibleActions(curState)
                if (actions):
                    for action in actions:
                        value_list.append(self.computeQValueFromValues(curState, action))
                    maxAction = max(value_list)
                    values_copy[curState] = maxAction
            for curState in state:
                self.values[curState] = values_copy[curState]
            
        # action = self.computeActionFromValues(self.values)
        "*** YOUR CODE HERE ***"
        


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        qVal = 0.0
        mdp = self.mdp
        discount = self.discount
        
        statesWithProb = mdp.getTransitionStatesAndProbs(state, action)
        for nextState, prob in statesWithProb:
            reward = mdp.getReward(state, action, nextState)
            stateVal = self.values[nextState]
            qVal = qVal + (reward + (prob * discount * stateVal))
            
        return qVal
        
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        mdp = self.mdp
        values = util.Counter()
        
        possibleActions = mdp.getPossibleActions(state)
        if (possibleActions == None):
            return None
        else:
            for action in possibleActions:
                qVal = self.computeQValueFromValues(state, action)
                values[action] = qVal
        actionMax = values.argMax()
        return actionMax

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        
        state = mdp.getStates()
        for i in range(self.iterations):
            curState = state[i % len(state)]
            value_list = []
            actions = mdp.getPossibleActions(curState)
            if (actions):
                for action in actions:
                    value_list.append(self.computeQValueFromValues(curState, action))
                maxAction = max(value_list)
                self.values[curState] = maxAction
            
        

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {}
        
        states = self.mdp.getStates()
        iterations = self.iterations
        priorityQueue = util.PriorityQueue()
        
        for state in states:
            if (self.mdp.isTerminal(state)):
                continue
            
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                statesWithProb = self.mdp.getTransitionStatesAndProbs(state, action)
                for nextState, prob in statesWithProb:
                    if (not predecessors.get(nextState)):
                        predecessors[nextState] = set()
                    if (prob > 0 and not self.mdp.isTerminal(nextState)):
                        predecessors[nextState].add(state)
                
            action = self.computeActionFromValues(state)
            maxQval = self.computeQValueFromValues(state, action)
            diff = abs(self.values[state] - maxQval)
            priorityQueue.push(state, -diff)
            
        for i in range(iterations):
            if (priorityQueue.isEmpty()):
                return
            state = priorityQueue.pop()
            if state is not 'TERMINAL_STATE':
                # actions = self.mdp.getPossibleActions(state)
                action = self.computeActionFromValues(state)
                self.values[state] = self.computeQValueFromValues(state, action)
                
                for p in predecessors[state]:
                    bestAction_a = self.computeActionFromValues(p)
                    maxQval = self.computeQValueFromValues(p, bestAction_a)
                    diff = abs(self.values[p] - maxQval)
                    if (diff > self.theta):
                        priorityQueue.update(p, -diff)
        return