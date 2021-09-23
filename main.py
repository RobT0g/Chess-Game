import pygame
from pygame.locals import *
from time import sleep

import InputManager
import ScreenManager
import BoardManager

pygame.init()                                                   # inicialização

screen_width = 800                                              # largura da tela
screen_height = 632                                             # altura da tela

screen = pygame.display.set_mode((screen_width, screen_height))     # tela definida
pygame.display.set_caption('Chess')                                 # legenda da tela

BoardManager.initialize()
ScreenManager.setonscreen(screen)
pygame.display.update()                                             # Atualizar o display

running = True                      # Variável de looping
while running:                      # looping
    event = pygame.event.wait()     # Esperando evento
    if InputManager.click():
        ScreenManager.update()                      # Atualiza a tela
        ScreenManager.setonscreen(screen)           # Coloca na tela
        m = ScreenManager.getmate()
        if m:
            if m[0]:
                ScreenManager.endscreen(True, screen)
            elif m[1]:
                ScreenManager.endscreen(False, screen)
        pygame.display.update()                     # Atualizando a tela
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:   # Fim do looping
        running = False
