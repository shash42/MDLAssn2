from MDP import State, Action, Transition
from lp2 import LP
import ValueIter

GAMMA = 0.999
DELTA = 1e-3 

ARR = [0.5, 1, 2]
X = 108 # team number 
Y = ARR[X % 3]

STEP_COST = -10.0/Y 
NEGATIVE_REWARD = -40

POSITIONS = ["W", "N", "E", "S", "C"]
MATERIALS = [0, 1, 2]
ARROWS = [0, 1, 2, 3]
MM = ["R", "D"]
HEALTH = [0, 25, 50, 75, 100]

ACTIONS = ["UP", "LEFT", "DOWN", "RIGHT", "STAY", "SHOOT", "HIT", "CRAFT", "GATHER", "NONE"]
ref = {}
states = {}
idx = 0 

CASE1 = 0
CASE2 = 0 
CASE3 = 0

# Add states
for p in POSITIONS:
    for m in MATERIALS:
        for a in ARROWS:
            for mm in MM:
                for h in HEALTH:
                    reward = 0 
                    state = (p, m, a, mm, h)

                    if h == 0:
                        reward = 50 
                        states[idx] = State(idx, reward, state, 1)
                    else :
                        states[idx] = State(idx, reward, state) 

                    ref[state] = idx 
                    idx += 1 

# Add actions 
for p in POSITIONS:
    for m in MATERIALS:
        for a in ARROWS:
            for mm in MM:
                for h in HEALTH:

                    cur = (p, m, a, mm, h)
                    now = ref[cur] 

                    if h == 0:
                        states[now].add_action(Action(now, "NONE"))
                        continue 

                    states[now].add_action(Action(now, "STAY"))

                    if p == "W":
                        states[now].add_action(Action(now, "RIGHT"))
                        if a > 0:
                            states[now].add_action(Action(now, "SHOOT"))

                    elif p == "E":
                        states[now].add_action(Action(now, "LEFT"))

                        states[now].add_action(Action(now, "HIT"))
                        if a > 0:
                            states[now].add_action(Action(now, "SHOOT"))

                    elif p == "S":
                        states[now].add_action(Action(now, "UP"))
                        states[now].add_action(Action(now, "GATHER"))

                    elif p == "C":
                        states[now].add_action(Action(now, "UP"))
                        states[now].add_action(Action(now, "RIGHT"))
                        states[now].add_action(Action(now, "DOWN"))
                        states[now].add_action(Action(now, "LEFT"))
                        
                        states[now].add_action(Action(now, "HIT"))
                        if a > 0:
                            states[now].add_action(Action(now, "SHOOT"))


                    elif p == "N":
                        states[now].add_action(Action(now, "DOWN"))
                        if m > 0:
                            states[now].add_action(Action(now, "CRAFT"))

# Add transitions 
for p in POSITIONS:
    for m in MATERIALS:
        for a in ARROWS:
            for mm in MM:
                for h in HEALTH:

                    cur = (p, m, a, mm, h)
                    now = ref[cur] 

                    # Terminal 
                    if h == 0 :
                        states[now].actions["NONE"].add_transition(now, 1, 0)
                        continue 

                    if p == "W":
                        nxt = ("C", m, a, mm, h)
                        pos = ref[nxt] 

                        # states[now].actions["STAY"].add_transition(now, 1)
                        # states[now].actions["RIGHT"].add_transition(pos, 1)
                        

                        # if a > 0:
                        #     states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.25)
                        #     states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h)], 0.75)

                        if mm == 'D':
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .8)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'R', h)], .2)
                            
                            states[now].actions["RIGHT"].add_transition(ref[("C", m, a, mm, h)], .8)
                            states[now].actions["RIGHT"].add_transition(ref[("C", m, a, 'R', h)], .2)
                            
                            if a > 0:
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.25 * .8)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'R', h - 25)], 0.25 * .2)

                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h)], 0.75 * .8)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'R', h)], 0.75 * .2)

                            
                        else:
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .5)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'D', h)], .5)
                            
                            states[now].actions["RIGHT"].add_transition(ref[("C", m, a, mm, h)], .5)
                            states[now].actions["RIGHT"].add_transition(ref[("C", m, a, 'D', h)], .5)
                            
                            if a > 0:
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.25 * .5)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'D', h - 25)], 0.25 * .5)

                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h)], 0.75 * .5)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'D', h)], 0.75 * .5)

                    elif p == "E":
                        if mm == "D" :
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .8)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'R', h)], .2)
                            
                            if not CASE1 :
                                states[now].actions["LEFT"].add_transition(ref[("C", m, a, mm, h)], .8)
                                states[now].actions["LEFT"].add_transition(ref[("C", m, a, 'R', h)], .2)
                            else :
                                states[now].actions["LEFT"].add_transition(ref[("W", m, a, mm, h)], .8)
                                states[now].actions["LEFT"].add_transition(ref[("W", m, a, 'R', h)], .2)

                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, max(0, h - 50) )], 0.2 * .8)
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, 'R', max(0, h - 50) )], 0.2 * .2)
                            
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, h)], 0.8 * .8)
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, 'R', h)], 0.8 * .2)
                            
                            if a > 0:
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.9 * .8)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'R', h - 25)], 0.9 * .2)

                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h)], 0.1 * .8)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'R', h)], 0.1 * .2)

                        else :
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .5)
                            states[now].actions["STAY"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            if not CASE1:
                                states[now].actions["LEFT"].add_transition(ref[("C", m, a, mm, h)], .5)
                                states[now].actions["LEFT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            else :
                                states[now].actions["LEFT"].add_transition(ref[("W", m, a, mm, h)], .5)
                                states[now].actions["LEFT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)

                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, max(0, h - 50) )], 0.2 * .5)
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, h)], 0.8 * .5)
                            states[now].actions["HIT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            
                            if a > 0:
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.9 * .5)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h)], 0.1 * .5)
                                
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)

                    elif p == "S":
                        nxt = ("C", m, a, mm, h)
                        pos = ref[nxt] 

                        e = ("E", m, a, mm, h)
                        epos = ref[e] 
                        

                        # states[now].actions["STAY"].add_transition(now, .85)
                        if mm == 'D':
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .85 * .8)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'R', h)], .85 * .2)

                            states[now].actions["STAY"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["STAY"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)

                            # states[now].actions["UP"].add_transition(pos, .85)
                            states[now].actions["UP"].add_transition(ref[("C", m, a, mm, h)], .85 * .8)
                            states[now].actions["UP"].add_transition(ref[("C", m, a, 'R', h)], .85 * .2)
                            
                            states[now].actions["UP"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["UP"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)
                            # states[now].actions["UP"].add_transition(epos, .15)

                            states[now].actions["GATHER"].add_transition(ref[(p, min(m+1, 2), a, mm, h)], 0.75 * .8)
                            states[now].actions["GATHER"].add_transition(ref[(p, min(m+1, 2), a, 'R', h)], 0.75 * .2)
                            
                            states[now].actions["GATHER"].add_transition(ref[(p, m, a, mm, h)], .25 * .8)
                            states[now].actions["GATHER"].add_transition(ref[(p, m, a, 'R', h)], .25 * .2)

                        else :
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .5 * .8)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'D', h)], .5 * .2)

                            states[now].actions["STAY"].add_transition(ref[("E", m, a, mm, h)], .5 * .8)
                            states[now].actions["STAY"].add_transition(ref[("E", m, a, 'D', h)], .5 * .2)

                            states[now].actions["UP"].add_transition(ref[("C", m, a, mm, h)], .5 * .8)
                            states[now].actions["UP"].add_transition(ref[("C", m, a, 'D', h)], .5 * .2)
                            
                            states[now].actions["UP"].add_transition(ref[("E", m, a, mm, h)], .5 * .8)
                            states[now].actions["UP"].add_transition(ref[("E", m, a, 'D', h)], .5 * .2)

                            states[now].actions["GATHER"].add_transition(ref[(p, min(m+1, 2), a, mm, h)], 0.5 * .8)
                            states[now].actions["GATHER"].add_transition(ref[(p, min(m+1, 2), a, 'D', h)], 0.5 * .2)
                            
                            states[now].actions["GATHER"].add_transition(ref[(p, m, a, mm, h)], .5 * .8)
                            states[now].actions["GATHER"].add_transition(ref[(p, m, a, 'D', h)], .5 * .2)

                    elif p == "C":
                        if mm == 'D' :
                            states[now].actions["RIGHT"].add_transition(ref[("E", m, a, mm, h)], .8)
                            states[now].actions["RIGHT"].add_transition(ref[("E", m, a, 'R', h)], .2)

                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .85 * .8)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'R', h)], .85 * .2)
                            
                            states[now].actions["STAY"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["STAY"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)
                            
                            states[now].actions["DOWN"].add_transition(ref[("S", m, a, mm, h)], .85 * .8)
                            states[now].actions["DOWN"].add_transition(ref[("S", m, a, 'R', h)], .85 * .2)
                            
                            states[now].actions["DOWN"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["DOWN"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)
                            
                            states[now].actions["LEFT"].add_transition(ref[("W", m, a, mm, h)], .85 * .8)
                            states[now].actions["LEFT"].add_transition(ref[("W", m, a, 'R', h)], .85 * .2)
                            
                            states[now].actions["LEFT"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["LEFT"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)
                            
                            states[now].actions["UP"].add_transition(ref[("N", m, a, mm, h)], .85 * .8)
                            states[now].actions["UP"].add_transition(ref[("N", m, a, 'R', h)], .85 * .2)
                            
                            states[now].actions["UP"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["UP"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)

                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, max(0, h - 50) )], 0.1 * .8)
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, 'R', max(0, h - 50) )], 0.1 * .2)
                            
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, h)], 0.9 * .8)
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, 'R', h)], 0.9 * .2)
                            
                            if a > 0:
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.5 * .8)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'R', h - 25)], 0.5 * .2)

                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h)], 0.5 * .8)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, 'R', h)], 0.5 * .2)

                        else :

                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .85 * .5)
                            states[now].actions["STAY"].add_transition(ref[("E", m, a, mm, h)], .15 * .5)
                            states[now].actions["STAY"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            states[now].actions["LEFT"].add_transition(ref[("W", m, a, mm, h)], .85 * .5)
                            states[now].actions["LEFT"].add_transition(ref[("E", m, a, mm, h)], .15 * .5)
                            states[now].actions["LEFT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            states[now].actions["RIGHT"].add_transition(ref[("E", m, a, mm, h)], .5)
                            states[now].actions["RIGHT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            states[now].actions["DOWN"].add_transition(ref[("S", m, a, mm, h)], .85 * .5)
                            states[now].actions["DOWN"].add_transition(ref[("E", m, a, mm, h)], .15 * .5)
                            states[now].actions["DOWN"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)


                            states[now].actions["UP"].add_transition(ref[("N", m, a, mm, h)], .85 * .5)
                            states[now].actions["UP"].add_transition(ref[("E", m, a, mm, h)], .15 * .5)
                            states[now].actions["UP"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)


                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, max(0, h - 50) )], 0.1 * .5)
                            states[now].actions["HIT"].add_transition(ref[(p, m, a, mm, h)], 0.9 * .5)
                            states[now].actions["HIT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            
                            if a > 0:
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.9 * .5)
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, a - 1, mm, h)], 0.1 * .5)
                                
                                states[now].actions["SHOOT"].add_transition(ref[(p, m, 0, 'D', min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)

                            


                    elif p == "N":
                        nxt = ("C", m, a, mm, h)
                        pos = ref[nxt] 

                        e = ("E", m, a, mm, h)
                        epos = ref[e] 
                        
                        # states[now].actions["STAY"].add_transition(now, .85)
                        # states[now].actions["STAY"].add_transition(epos, .15)

                        # states[now].actions["DOWN"].add_transition(pos, .85)
                        # states[now].actions["DOWN"].add_transition(epos, .15)

                        # if m > 0:
                        #     states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 1), mm, h)], 0.5)
                        #     states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 2), mm, h)], 0.35)
                        #     states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 3), mm, h)], 0.15)

                        if mm == 'D':
                            
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .85 * .8)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'R', h)], .85 * .2)

                            states[now].actions["STAY"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["STAY"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)

                            # states[now].actions["UP"].add_transition(pos, .85)
                            states[now].actions["DOWN"].add_transition(ref[("C", m, a, mm, h)], .85 * .8)
                            states[now].actions["DOWN"].add_transition(ref[("C", m, a, 'R', h)], .85 * .2)
                            
                            states[now].actions["DOWN"].add_transition(ref[("E", m, a, mm, h)], .15 * .8)
                            states[now].actions["DOWN"].add_transition(ref[("E", m, a, 'R', h)], .15 * .2)

                            # states[now].actions["STAY"].add_transition(now, .85)
                            # states[now].actions["STAY"].add_transition(epos, .15)

                            # states[now].actions["DOWN"].add_transition(pos, .85)
                            # states[now].actions["DOWN"].add_transition(epos, .15)

                            if m > 0:
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 1), mm, h)], 0.5 * .8)
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 1), 'R', h)], 0.5 * .2)

                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 2), mm, h)], 0.35 * .8)
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 2), 'R', h)], 0.35 * .2)

                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 3), mm, h)], 0.15 * .8)
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 3), 'R', h)], 0.15 * .2)

                        else :
                            
                            
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, mm, h)], .85 * .5)
                            states[now].actions["STAY"].add_transition(ref[(p, m, a, 'D', h)], .85 * .5)

                            states[now].actions["STAY"].add_transition(ref[("E", m, a, mm, h)], .15 * .5)
                            states[now].actions["STAY"].add_transition(ref[("E", m, a, 'D', h)], .15 * .5)

                            # states[now].actions["UP"].add_transition(pos, .85)
                            states[now].actions["DOWN"].add_transition(ref[("C", m, a, mm, h)], .85 * .5)
                            states[now].actions["DOWN"].add_transition(ref[("C", m, a, 'D', h)], .85 * .5)
                            
                            states[now].actions["DOWN"].add_transition(ref[("E", m, a, mm, h)], .15 * .5)
                            states[now].actions["DOWN"].add_transition(ref[("E", m, a, 'D', h)], .15 * .5)
                            
                            # states[now].actions["STAY"].add_transition(now, .85)
                            # states[now].actions["STAY"].add_transition(epos, .15)

                            # states[now].actions["DOWN"].add_transition(pos, .85)
                            # states[now].actions["DOWN"].add_transition(epos, .15)

                            if m > 0:
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 1), mm, h)], 0.5 * .5)
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 1), 'D', h)], 0.5 * .5)

                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 2), mm, h)], 0.35 * .5)
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 2), 'D', h)], 0.35 * .5)

                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 3), mm, h)], 0.15 * .5)
                                states[now].actions["CRAFT"].add_transition( ref[(p, m - 1, min(3, a + 3), 'D', h)], 0.15 * .5)
                        

def case2():
    global states 
    for i, s in states:
        for t in s.actions["STAY"].transitions:
            t.reward = 0 
    return 


# GAMMA = 0.25 
#ValueIter.solve(states, GAMMA, DELTA, 0, "Case 0 Trace.txt")
print(STEP_COST)

def simulate(state):
    start_state = state 
    print('START STATE:', start_state)
    cumalative_reward = 0
    idx = ref[start_state]

    iterations = 0
    MAX_ITERATIONS = 100
    discount = 1 

    # print(states[idx].get_best_action().name)
    while not states[idx].terminal :
        cur = states[idx] 
        action = cur.get_best_action()
        idx, r = action.take_action()
        nxt = states[idx] 
        cumalative_reward += discount * r 
        print(cur.repr, action.name, nxt.repr, round(cumalative_reward, 3)) 

        if iterations > MAX_ITERATIONS :
            print("End state not reached")
            return 

        iterations += 1 
        discount *= GAMMA 

    cumalative_reward += 50 
    print("Overall Reward:", round(cumalative_reward, 3))
    
def simulateLP(start_state):
    model = LP(states, GAMMA, STEP_COST, ref[start_state])
    model.execute()


# start_state = ('W', 0, 0, 'D', 100)
start_state = ('C', 2, 0, 'R', 100) 
#simulate(start_state)
simulateLP(start_state)