from MDP import State, Action, Transition
import ValueIter

y = 0.2
e = 0.01
reward = 15
#Add states
states = {"A" : State("A"), "B" : State("B"), "C" : State("C"), "R" : State("R", reward, 1)}

#Add actions
states["A"].add_action(Action("A", "rt"))
states["A"].add_action(Action("A", "up"))
states["B"].add_action(Action("B", "lt"))
states["B"].add_action(Action("B", "up"))
states["C"].add_action(Action("C", "rt"))
states["C"].add_action(Action("C", "dn"))

#Add transitions A
states["A"].actions["rt"].add_transition("B", 0.8, -1)
states["A"].actions["rt"].add_transition("A", 0.2, -1)
states["A"].actions["up"].add_transition("C", 0.8, -1)
states["A"].actions["up"].add_transition("A", 0.2, -1)

#Add transitions B
states["B"].actions["lt"].add_transition("A", 0.8, -1)
states["B"].actions["lt"].add_transition("B", 0.2, -1)
states["B"].actions["up"].add_transition("R", 0.8, -4)
states["B"].actions["up"].add_transition("B", 0.2, -1)

#Add transitions C
states["C"].actions["rt"].add_transition("R", 0.25, -3)
states["C"].actions["rt"].add_transition("C", 0.75, -1)
states["C"].actions["dn"].add_transition("A", 0.8, -1)
states["C"].actions["dn"].add_transition("C", 0.2, -1)

for transition in states["A"].actions["rt"].transitions:
    print(transition.source, transition.action, transition.dest)

ValueIter.solve(states, y, e, 1)