import pygame
from pygame.locals import *


pygame.init()   # Inicialização
pxy = [0, 0]    # Posição do mouse
pos = [0, 0]    # Posição do mouse em relação ao tabuleiro


def secl():         # Atualização e retone da posição do mouse em relação ao tabuleiro
    global pos
    global pxy
    pxy = [pygame.mouse.get_pos()[0]-16, pygame.mouse.get_pos()[1]-16]
    if (pxy[0] in range(0, 632)) and (pxy[1] in range(0, 632)):
        pos[0] = int(pxy[0]/75)
        pos[1] = int(pxy[1]/75)
    return pos


def clickable():    # Define se o mouse está dentro da hitbox de uma tecla
    secl()
    global pxy
    if (pxy[0] % 75 >= 10) and (pxy[0] % 75 <= 65) and (pxy[1] % 75 >= 10) and (pxy[1] % 75 <= 65):
        if (pxy[0] in range(0, 632)) and (pxy[1] in range(0, 632)):
            return True
    return False


def click():        # Retorna o estado do mouse
    return pygame.mouse.get_pressed(num_buttons=3)[0]


def getpos():       # Retorna a posição do mouse
    return pxy
