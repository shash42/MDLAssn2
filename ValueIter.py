from MDP import State, Action, Transition

def state_print(states, iter=-1):
    if iter != -1:
        print(f"Iteration: {iter}")
    for state in states.values():
        print(state.name, state.value)
    print("----------")

def solve(states, y, e, printer=0):
    INF = 1e15
    iter = 0
    while True:
        if iter>10:
            print("Hard break")
            break

        if printer != 0:
            state_print(states, iter)

        max_change = 0
        updates = {}

        for state in states.values():
            if state.terminal == 1:
                continue

            best_action = [-INF, None]

            for action in state.actions.values():
                action.qvalue = 0

                for transition in action.transitions:
                    action.qvalue +=  transition.prob * (y*states[transition.dest].value + transition.reward)
                if iter==0:
                    print(state.name, action.name, transition.dest, action.qvalue)
                if action.qvalue > best_action[0]:
                    best_action = [action.qvalue, action]
            
            updates.update({state.name : best_action})

        for name, best_action in updates.items():
            if best_action[1] is None:
                continue
            value = best_action[0]

            change = abs(value - states[name].value)
            if change > max_change:
                max_change = change
            states[name].value = value

        if max_change < e:
            print(f"Stopping: Delta = {max_change}")
            print(f"Last Iteration: {iter+1}")
            for state in states.values():
                action_name = "End"
                if state.terminal == 0:
                    action_name = updates[state.name][1].name
                print(state.name, state.value, action_name)
            print("----------")
            break

        iter+=1

    return states