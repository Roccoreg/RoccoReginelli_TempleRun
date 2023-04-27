# File created by Rocco Reginelli

# import libs
import pygame as pg
import os
# import settings 
from Settings import *
from Sprites import *
# from pg.sprite import Sprite

import pygame

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (220,220,220)
BLUE = (176,0,230)

# Set the dimensions of the screen
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 850
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the game window
pygame.display.set_caption("My Game")

# Load the character image
character_image = pygame.image.load("character.png")
new_width = 40
new_height = 40
character_image = pygame.transform.scale(character_image, (new_width, new_height))
# Create a character class
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = character_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 100

    def update(self):
        pass

# Create a group to hold the character
all_sprites_group = pygame.sprite.Group()

# Create a character and add it to the group
character = Character()
all_sprites_group.add(character)

# Set up the game loop
clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(BLACK)

    # Update the sprites
    all_sprites_group.update()

    # Draw the sprites
    all_sprites_group.draw(screen)

    # Update the display
    pygame.display.flip()

    # Set the FPS of the game
    clock.tick(60)


# Quit Pygame
pygame.quit()