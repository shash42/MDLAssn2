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

    def add_transition(self, dest, prob, reward):
        self.transitions.append(Transition(self.source, self.name, dest, prob, reward))

class State:
    def __init__(self, name, value=0, terminal=0):
        self.name = name
        self.value = value
        self.terminal = terminal
        self.actions = {}

    def add_action(self, action):
        self.actions.update({action.name : action})

