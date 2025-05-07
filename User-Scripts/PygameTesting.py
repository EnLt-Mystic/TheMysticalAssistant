import pygame
from pygame.locals import *

COLOURS = {
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "yellow" : (255, 255, 0),
    "cyan" : (0, 255, 255),
    "magenta" : (255, 0, 255),
    "black" : (0, 0, 0),
    "grey" : (127, 127, 127),
    "white" : (255, 255, 255)
}

running = True

pygame.init()

surface = pygame.display.set_mode((480, 540))
pygame.display.set_caption("J.A.R.V.I.S.")

while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

pygame.quit()



