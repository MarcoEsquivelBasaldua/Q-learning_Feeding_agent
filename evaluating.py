import numpy as np

##### Load trined Q-table ###
Q = np.load('Q-table.npy', allow_pickle= True)
print(Q.item().get((0, 0, 0, 0)))

### Hyperparameters ####
MAX_STEPS = 100
