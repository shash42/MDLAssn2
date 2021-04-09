from MDP import State, Transition, Action

class LP:
    def __init__(self, states, y, e):
        self.states = states
        self.y = y
        self.e = e
        self.dim = self.get_tot_actions()
        self.r = self.get_r()
        self.a = self.get_a()
        self.alpha = self.get_alpha()
        self.x = self.quest()
        self.policy = []
        self.solution_dict = {}
        self.objective = 0.0
        name_idx_map = {}
        idx = 0
        for name, s in self.states.items():
            name_idx_map.update(name, idx)
            idx += 1

    def getidx_of_state(self, name):
        return name_idx_map[name]
    
    def get_tot_actions(self):
        tot_actions = 0
        for s, name in self.states.items():
            tot_actions = tot_actions + len(s.actions)
        return tot_actions

    def get_a(self):
        a = np.zeros((len(self.states), self.dim), dtype=np.float64)

        idx = 0
        i=0
        for name, s in self.states.items():
            for action in s.actions:
                a[i][idx] += 1
                next_states = []
                for trans in action.transitions:
                    next_states.append(trans)
                
                for next_state in next_states:
                    a[next_state.dest][idx] -= next_state.prob #next_state.dest should hash to an index

                # increment idx
                idx += 1
                i += 1

        return a

    def get_r(self):
        r = np.full((1, self.dim), COST) #change here

        idx = 0
        for name, s in self.states.items():
            for action in s.actions:
                #change from here
                if action == ACT_NOOP:
                    r[0][idx] = 0
                idx += 1
        
        return r

    def get_alpha(self):
        alpha = np.zeros((NUM_STATES, 1))
        s = State(HEALTH_VALUES[-1], ARROWS_VALUES[-1], STAMINA_VALUES[-1]).get_hash()
        alpha[s][0] = 1
        return alpha

    def quest(self):
        x = cp.Variable((self.dim, 1), 'x')
        
        constraints = [
            cp.matmul(self.a, x) == self.alpha,
            x >= 0
        ]

        objective = cp.Maximize(cp.matmul(self.r, x))
        problem = cp.Problem(objective, constraints)

        solution = problem.solve()
        self.objective = solution
        arr = list(x.value)
        l = [ float(val) for val in arr]
        return l

    def get_policy(self):
        idx = 0
        for i in range(NUM_STATES):
            s = State.from_hash(i)
            actions = s.actions()
            act_idx = np.argmax(self.x[idx : idx+len(actions)])
            idx += len(actions)
            best_action = actions[act_idx]
            local = []
            local.append(s.as_list())
            local.append(ACTION_NAMES[best_action])
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