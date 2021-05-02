import pygame
import numpy as np

##### Load trined Q-table ###
Q = np.load('Q-table.npy', allow_pickle=True)

#### initialize pygame #########
SIZE = 700
pygame.init()
pygame.display.set_caption('Feedding game')
screen = pygame.display.set_mode((SIZE,SIZE))

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

escale = SIZE//10
############# Used Functions ###################
# Given pos in discrete grid coordinates, returns location on the screen (pixels) coordinates
def to_mapCoordinates(pos):
    return escale * np.flipud(pos)# + escale//2


############# Game Loop #################
running = True
game_time = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    screen.fill(WHITE)
    for i in range(1,10):
        pygame.draw.line(screen, GRAY, (0,i*escale), (SIZE-1, i*escale), 3)
    for i in range(1,10):
        pygame.draw.line(screen, GRAY, (i*escale,0), (i*escale,SIZE-1), 3)

    pos = to_mapCoordinates(np.array([0,0], dtype=int))
    screen.blit(Player, pos)



    pygame.display.update()
    pygame.time.delay(game_time)