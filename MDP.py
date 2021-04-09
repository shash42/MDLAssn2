ARR = [0.5, 1, 2]
X = 108 # team number 
Y = ARR[X % 3]

STEP_COST = -10.0/Y 
#STEP_COST = -10.0

import numpy as np 

class Transition:
    def __init__(self, source, action, dest, prob, reward):
        self.source, self.action = source, action
        self.dest, self.prob, self.reward = dest, prob, reward

class Action:
    def __init__(self, source, name, qvalue=0):
        self.source = source
        self.name = name
        self.qvalue = qvalue
        self.transitions = []

    def add_transition(self, dest, prob, reward=STEP_COST):
        self.transitions.append(Transition(self.source, self.name, dest, prob, reward))

    def take_action(self):
        rnd = np.random.random() 
        prefix = 0 
        for t in self.transitions:
            prefix += t.prob 
            if rnd <= prefix :
                return t.dest, t.reward 

class State:
    def __init__(self, name, value=0, repr = "", terminal=0):
        self.name = name
        self.repr = repr
        self.value = value
        self.terminal = terminal
        self.actions = {}

    def add_action(self, action):
        self.actions.update({action.name : action})

    def get_best_action(self):
        qvals = []
        bestQ = -1e9
        bestAct = None 
        for action_pair in self.actions.values():
            # action = action_pair.values()[0] 
            action = action_pair 
            qval = action.qvalue 

            if qval > bestQ:
                bestQ = qval
                bestAct = action 

        return bestAct 

        


