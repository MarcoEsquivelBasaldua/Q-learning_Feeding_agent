import numpy as np
from numpy import random
from numpy.lib.function_base import place

#### Hyperparameters ####
SIZE = 10
ACTION_SPACE = 9
TOTAL_EPISODES = int(1e5)

MAX_STEPS = 10 #STATE_SPACE

LEARNING_RATE = 0.01
GAMMA = 0.99

MAX_EPSILON = 1.0
MIN_EPSILON = 0.001
DECAY_RATE = 0.01

#### Q table as a dictionary ####
Q = {}
for i_player in range(SIZE):
    for j_player in range(SIZE):
        for i_food in range(SIZE):
            for j_food in range (SIZE):
                actions = np.zeros(ACTION_SPACE)
                Q[(i_player,j_player,i_food,j_food)] = actions

############ Epsilon-Greedy policy ##############
def epsilon_greedy_policy(state, epsilon):
    if np.random.uniform(0,1) > epsilon:
        action = np.argmax(Q[state])
    else:
        action = np.random.randint(0, ACTION_SPACE)

    return action

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
        # player steps out the environment
        done = True
        new_state = 0
        if not (0 <= self.player[0] < SIZE) or not(0 <= self.player[1] < SIZE):
            reward = -200
        else:
            if (self.player == self.food).all():
                reward = 10
            else:
                reward = -1
                new_state = np.array([self.player, self.food])
                new_state = np.reshape(new_state, (1,4))[0]
                done =  False

                new_state = tuple(new_state)

        return new_state, reward, done


#### Q-learning algorithm and training ####
env = Environment()
SHOW_EVERY = 500

for episode in range(TOTAL_EPISODES):
    if episode % SHOW_EVERY == 0 or episode == TOTAL_EPISODES-1:
        print('Episode:', episode)
    # Reset environment
    state = env.reset()

    # Reduce epsilon
    epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-DECAY_RATE * episode-1)

    for step in range(MAX_STEPS):
        action = epsilon_greedy_policy(state, epsilon)

        # Take action and observe outcome state and reward
        new_state, reward, done = env.step(action)

        # Update Q(s,a) <- Q(s,a) + lr [R(s,a) + gamma * max(Q(s',a')) - Q(s,a)]
        try:
            Q[state][action] = Q[state][action] + LEARNING_RATE * (reward + GAMMA * np.max(Q[new_state]) - Q[state][action])
        except:
            pass

        if done:
            break

        state = new_state

# Save Q table
np.save('Q-table.npy',Q)