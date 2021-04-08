from MDP import State, Action, Transition
import sys 

def state_print(states, iter=-1):
    if iter != -1:
        print(f"iteration={iter}")
    for state in states.values():
        a, b, c, d, e = state.repr 
        # print("({a},{b},{c},{d},{e}):{"
        print(state.name, state.value)
    print("----------")

def solve(states, y, e, printer=0):
    INF = 1e15
    iter = 0

    f = open("Part2Trace1.txt", "w")
    while True:
        if iter>150:
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
                # if iter==0:
                #     print(state.name, action.name, transition.dest, action.qvalue)
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


        # print(f"Stopping: Delta = {max_change}")
        # print(f"Last Iteration: {iter+1}")
        og = sys.stdout 
        sys.stdout = f 

        print(f"iteration={iter}")
        for state in states.values():
            action_name = "NONE"
            if state.terminal == 0:
                action_name = updates[state.name][1].name
            
            a, b, c, d, w = state.repr 
            val = round(state.value, 3)
            print(f"({a},{b},{c},{d},{w}):{action_name}=[{val}]")

            # print(state.repr, state.value, action_name)
        # print("----------")
        sys.stdout = og 
        
        print(max_change, iter)
        if max_change < e:
            break

        iter+=1

    f.close()
    return states