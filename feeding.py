import pygame
import numpy as np

##### Load trined Q-table ###
Q = np.load('Q-table.npy', allow_pickle=True)

#### initialize pygame #########
pygame.init()
pygame.display.set_caption('Feedding game')
screen = pygame.display.set_mode((600,600))

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150,150,150)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (190,230,90)
PURPLE = (148,0,188)


############# Game Loop #################
running = True
game_time = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    screen.fill(WHITE)
    escale = 60
    for i in range(1,10):
        pygame.draw.line(screen, GRAY, (0,i*escale), (600-1, i*escale), 3)
    for i in range(1,10):
        pygame.draw.line(screen, GRAY, (i*escale,0), (i*escale,600-1), 3)



    pygame.display.update()
    pygame.time.delay(game_time)