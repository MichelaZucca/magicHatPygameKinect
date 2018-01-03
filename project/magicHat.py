#/usr/bin/python

import sys, pygame
import numpy as np

pygame.init()

size = width, height = 1024, 728
speed = [1.0, 1.0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

hat = pygame.image.load('images/magicHat.png')
hat = pygame.transform.scale(hat, (150,150))
hatrect = hat.get_rect()
hatrect.center = (512,600)

background = pygame.image.load('images/background.jpg');
background = pygame.transform.scale(background, (1024,728))

backgroundrect = background.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    inHat = 0
    outHat = 0
    if hatrect.collidepoint(pygame.mouse.get_pos()):
        print('Dans le chapeau')
        magicImage = pygame.image.load('images/1.png')
        magicImage = pygame.transform.scale(magicImage, (100,100))
        pos = magicImage.get_rect(center = screen.get_rect().center)
        screen.blit(magicImage, pos)
        pygame.display.flip()
    else :
        screen.fill(black)
        screen.blit(background, backgroundrect)
        screen.blit(hat, hatrect)
        pygame.display.flip()
