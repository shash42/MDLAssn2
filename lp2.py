from MDP import State, Transition, Action
import numpy as np
import cvxpy as cp
import os, json

ACTIONS = ["UP", "LEFT", "DOWN", "RIGHT", "STAY", "SHOOT", "HIT", "CRAFT", "GATHER", "NONE"]

class LP:
    def __init__(self, states, y, STEP_COST, init_state):
        self.name_idx_map = {}
        self.states = states
        idx = 0
        for name, s in self.states.items():
            self.name_idx_map.update({name : idx})
            idx+=1

        self.y = y
        self.init_state = self.states[init_state]
        self.dim = self.get_tot_actions()
        self.r = self.get_r()
        self.a = self.get_a()
        self.alpha = self.get_alpha()
        print(self.r.shape, self.a.shape, self.alpha.shape)
        self.x = self.quest()
        self.policy = []
        self.solution_dict = {}
        self.objective = 0.0
        self.step_cost = STEP_COST

    def getidx_of_state(self, name):
        return self.name_idx_map[name]

    def get_tot_actions(self):
        tot_actions = 0
        for name,s in self.states.items():
            tot_actions = tot_actions + len(s.actions)
        return tot_actions

    def get_a(self):
        a = np.zeros((len(self.states), self.dim), dtype=np.float64)

        idx = 0
        i = 0
        for name, s in self.states.items():
            for a_name, action in s.actions.items():
                a[i][idx] += 1
                next_states = []
                for trans in action.transitions:
                    next_states.append(trans)
                
                for next_state in next_states:
                    dest_idx = self.getidx_of_state(next_state.dest)
                    if dest_idx == i:
                        continue
                    a[dest_idx][idx] -= next_state.prob

                # increment idx
                idx += 1
            i += 1

        return a

    def get_r(self):
        r = np.zeros((1, self.dim)) #change here

        idx = 0
        for name, s in self.states.items():
            for action_name in s.actions:
                #change from here
                if action_name == "NONE":
                    r[0][idx] = 0
                    idx += 1
                    continue
            
            for name, action in s.actions.items():
                # r[0][idx] += self.step_cost
                for trans in action.transitions:
                    r[0][idx] += trans.prob * trans.reward
       
        return r

    def get_alpha(self):
        alpha = np.zeros((len(self.states), 1))
        s = self.getidx_of_state(self.init_state.name) # starting state idx
        alpha[s][0] = 1
        return alpha

    def quest(self):
        x = cp.Variable((self.dim, 1))
        
        constraints = [
            cp.matmul(self.a, x) == self.alpha,
            x >= 0
        ]

        objective = cp.Maximize(cp.matmul(self.r, x))
        problem = cp.Problem(objective, constraints)

        solution = problem.solve()
        self.objective = solution
        #print(x)
        print(x.value)
        print(self.objective)
        arr = list(x.value)
        l = [ float(val) for val in arr]
        return l

    def get_policy(self):
        idx = 0
        for name, s in self.states.items():
            #s = State.from_hash(i)
            actions = s.actions
            act_idx = np.argmax(self.x[idx : idx+len(actions)])
            best_action = act_idx# - idx
            #print(f"{best_action}")
            idx += len(actions)
            
            #best_action = actions[act_idx]
            local = []
            local.append(s.repr)
            local.append(ACTIONS[best_action]) ## change??
            self.policy.append(local)

    def generate_dict(self):
        self.solution_dict["a"] = self.a.tolist()
        r = [float(val) for val in np.transpose(self.r)]
        self.solution_dict["r"] = r
        alp = [float(val) for val in self.alpha]
        self.solution_dict["alpha"] = alp
        self.solution_dict["x"] = self.x
        self.solution_dict["policy"] = self.policy
        self.solution_dict["objective"] = float(self.objective)
        
    def write_output(self):
        path = "outputs/output.json"
        json_object = json.dumps(self.solution_dict, indent=4)
        with open(path, 'w+') as f:
          f.write(json_object)

    def execute(self):
        os.makedirs('outputs', exist_ok=True)
        self.quest()
        self.get_policy()
        self.generate_dict()
        self.write_output()
