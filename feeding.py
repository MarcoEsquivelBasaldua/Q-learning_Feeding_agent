import pygame
import numpy as np
import copy

##### Load trined Q-table ###
#with open('Q_table.json', 'r') as f:
#    Q = json.load(f)
Q = np.load('Q-table.npy', allow_pickle= True)
print(type(Q))
#print(Q.item().get((0, 0, 0, 0)))


#### initialize pygame #########
SIZE = 10
SIZE_MAP = 700
pygame.init()
pygame.display.set_caption('Feedding game')
screen = pygame.display.set_mode((SIZE_MAP,SIZE_MAP))

Player = pygame.image.load('zombie.png')
Player_rect = Player.get_rect()
Food = pygame.image.load('screaming.png')
Food_rect = Food.get_rect()

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150,150,150)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (190,230,90)
PURPLE = (148,0,188)

escale = SIZE_MAP//10
############# Used Functions ###################
# Given pos in discrete grid coordinates, returns location on the screen (pixels) coordinates
def to_mapCoordinates(pos):
    return escale * np.flipud(pos)# + escale//2


class Environment:
    def __init__(self):
        self.player_pos = np.array([0,0], dtype=int)
        self.food_pos = np.array([0,0], dtype=int)

    def get_state(self):
        state = np.array([self.player_pos, self.food_pos])
        state = np.reshape(state, (1,4))[0]
        
        return tuple(state)

    def draw(self):
        screen.fill(WHITE)
        for i in range(1,10):
            pygame.draw.line(screen, GRAY, (0,i*escale), (SIZE_MAP-1, i*escale), 3)
        for i in range(1,10):
            pygame.draw.line(screen, GRAY, (i*escale,0), (i*escale,SIZE_MAP-1), 3)

        Player_map = to_mapCoordinates(self.player_pos)
        Food_map = to_mapCoordinates(self.food_pos)

        screen.blit(Player, Player_map)
        screen.blit(Food, Food_map)


    def respawn(self):
        rand_state = np.random.randint(low=0, high=10, size=4)
        self.player_pos = rand_state[0:2]
        self.food_pos = rand_state[2:4]

        return tuple(rand_state)

    def food_move(self):
        action =  np.random.randint(low=0, high=8, size=1)
        pos = copy.deepcopy(self.food_pos)
        
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
            self.food_pos = pos


    def player_move(self, action):
        if action == 1:
            self.player_pos += np.array((0, 1))
        elif action == 2:
            self.player_pos += np.array((-1, 1))
        elif action == 3:
            self.player_pos += np.array((-1, 0))
        elif action == 4:
            self.player_pos += np.array((-1, -1))
        elif action == 5:
            self.player_pos += np.array((0, -1))
        elif action == 6:
            self.player_pos += np.array((1, -1))
        elif action == 7:
            self.player_pos += np.array((1, 0))
        elif action == 8:
            self.player_pos += np.array((1, 1))


############# Game Loop #################
running = True
game_time = 500
step = 0
env = Environment()
state = env.respawn()

env.draw()
pygame.display.update()
pygame.time.delay(game_time)

steps = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if pygame.key.get_pressed()[13] == 1: # Start a new game
            state = env.respawn()
            steps = 0


    
    if (env.player_pos == env.food_pos).all():
        print('End of the game in ', steps)

    else:
        steps += 1

        ## Food moves
        env.food_move()

        # Player moves
        state = env.get_state()
        action = np.argmax(Q.item().get(state))
        env.player_move(action)


    env.draw()


    pygame.display.update()
    pygame.time.delay(game_time)