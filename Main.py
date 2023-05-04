# File created by Rocco Reginelli

import pygame

pygame.init()

# Library of game contants
White = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
WIDTH = 400
HEIGHT = 500
background = White
player = pygame.transform.scale(pygame.image.load('doodle.png'), (90,70))
fps = 60
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()

# Game variables
player_x = 170
player_y = 400
platforms = {[175, 480, 70, 10]}
# create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Doodle Jumper')

running = True
while running == True:
    timer.tick(fps)
    screen.fill(background)
    screen.blit(player, (player_x, player_y))
    blocks = []

    for i in range(len(platforms)):
        block = pygame.dra.rect(screen, black, platforms[i])
blocks.append(block)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit

