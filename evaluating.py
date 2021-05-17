import numpy as np
import matplotlib.pyplot as plt
import copy

##### Load trined Q-table ###
Q = np.load('Q-table.npy', allow_pickle= True)
# print(Q.item().get((0, 0, 0, 0)))
# state = (0, 0, 0, 0)
# action = np.argmax(Q.item().get(state))
# print(action)

### Hyperparameters ####
MAX_STEPS = 100
GAMMA = 0.99
SIZE = 10
n_bins = 10


###### Environment #####
class Environment:
    def __init__(self):
        self.player = []
        self.food = []

    def reset(self):
        # Position player and food randomly
        rand_state = np.random.randint(low=0, high=SIZE, size=4)
        self.player = rand_state[0:2]
        self.food = rand_state[2:4]

        #return tuple(map(tuple, rand_state))
        return tuple(rand_state)

    def get_state(self):
        state = np.array([self.player, self.food])
        state = np.reshape(state, (1,4))[0]

        return tuple(state)

    def set_state(self, state):
        self.player = np.array(state[0:2])
        self.food = np.array(state[2:4])

    def food_move(self):
        action =  np.random.randint(low=0, high=8, size=1)
        pos = copy.deepcopy(self.food)
        
        if action == 1:
            pos += np.array((0, 1))
        elif action == 2:
            pos += np.array((-1, 1))
        elif action == 3:
            pos += np.array((-1, 0))
        elif action == 4:
            pos += np.array((-1, -1))
        elif action == 5:
            pos += np.array((0, -1))
        elif action == 6:
            pos += np.array((1, -1))
        elif action == 7:
            pos += np.array((1, 0))
        elif action == 8:
            pos += np.array((1, 1))

        if (0 <= pos[0] < SIZE) and (0 <= pos[1] < SIZE):
            self.food = pos

    def step(self, action):
        if action == 1:
            self.player += np.array((0, 1))
        elif action == 2:
            self.player += np.array((-1, 1))
        elif action == 3:
            self.player += np.array((-1, 0))
        elif action == 4:
            self.player += np.array((-1, -1))
        elif action == 5:
            self.player += np.array((0, -1))
        elif action == 6:
            self.player += np.array((1, -1))
        elif action == 7:
            self.player += np.array((1, 0))
        elif action == 8:
            self.player += np.array((1, 1))

        # Rewards
        done = True
        # player steps out the environment
        if not (0 <= self.player[0] < SIZE) or not(0 <= self.player[1] < SIZE):
            reward = -200
        else:
            if (self.player == self.food).all():
            #if self.player == self.food:
                reward = 10
            else:
                reward = -1
                
                done =  False

        new_state = np.array([self.player, self.food])
        new_state = np.reshape(new_state, (1,4))[0]
        new_state = tuple(new_state)

        return new_state, reward, done

env = Environment()
V_vals_hist = []

total_samples = 100
samples = []

for s in range(total_samples):
    samples.append(env.reset())


for Q_current in Q:

    V_vals = []

    for state in samples:
        env.set_state(state)
        
        v_t = 0.

        for step in range(MAX_STEPS):
            state = env.get_state()

            action = np.argmax(Q_current[state])

            new_state, reward, done = env.step(action)

            v_t += GAMMA**step * reward

            if done:
                break

            env.food_move()
        V_vals.append(v_t)

    V_vals_hist.append(V_vals)


hist_episodes = np.loadtxt('Q-tables_historial_episodes.txt', dtype=int)

plt.figure(figsize=(20,6))
TOTAL_QTABLES = 5
for i in range(TOTAL_QTABLES):
    plt.hist(V_vals_hist[i], bins=n_bins, alpha=0.5, label="Episode"+str(hist_episodes[i]))

# plt.figure(figsize=(20,6))
# for V in V_vals_hist:
#     plt.hist(V, bins=n_bins, alpha=0.5, label="data1")


# plt.figure(figsize=(8,6))
# plt.hist(V_vals_hist[0], bins=n_bins, alpha=0.5, label="data1")
# plt.hist(V_vals_hist[1], bins=n_bins, alpha=0.5, label="data2")

plt.xlabel("Data", size=14)
plt.ylabel("Count", size=14)
plt.title("Multiple Histograms with Matplotlib")
plt.legend(loc='upper right')
  
# Show plot
plt.show()
