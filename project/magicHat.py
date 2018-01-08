# /usr/bin/python

import sys, pygame
import numpy as np
from random import randint

pygame.init()

size = width, height = 1024, 728
black = 0, 0, 0

# Fenêtre du jeu
screen = pygame.display.set_mode(size)

# Chapeau du magicien
hat = pygame.image.load('images/magicHat.png')
hat = pygame.transform.scale(hat, (150, 150))
hatrect = hat.get_rect()
hatrect.center = (512, 600)

# Background du jeu
background = pygame.image.load('images/background.jpg');
background = pygame.transform.scale(background, (1024, 728))
backgroundrect = background.get_rect()

inHat = 0  # Détection de la souris dans le chapeau
counter = 0  # temps d'affichage de l'objet magique sortie du chapeau
timeMax = 200  # temps maximum d'affichage
randomActif = 1  # Sélection d'une nouvelle image

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Souris détectée dans le rectangle du chapeau
    if hatrect.collidepoint(pygame.mouse.get_pos()):
        inHat = 1 # dans le chapeau
        # tirage de l'image aléatoire
        if randomActif > 0:
            no = randint(1, 8)
            randomActif = 0
        # chemin d'accès de l'image
        srcImage = 'images/' + str(no) + '.png'
    # Souris en dehors du chapeau
    else:
        if inHat > 0 and counter < timeMax:
            # chargement des étoiles autour de l'objet magiques
            stars = pygame.image.load('images/stars.gif')
            starsrect = stars.get_rect(center=screen.get_rect().center)
            # chargement de l'objet magique
            img = pygame.image.load(srcImage)
            img = pygame.transform.scale(img, (150, 150))
            imgrect = img.get_rect(center=screen.get_rect().center)
            screen.blit(stars, starsrect)
            screen.blit(img, imgrect)
            pygame.display.flip()
            counter += 1
        else:
            # reset des variables
            inHat = 0
            randomActif = 1
            counter = 0
            # affichage de l'écran de jeu de base
            screen.fill(black)
            screen.blit(background, backgroundrect)
            screen.blit(hat, hatrect)
            pygame.display.flip()
