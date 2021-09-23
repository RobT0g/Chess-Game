import BoardManager
import pygame
from pygame.locals import *


pygame.font.init()

board = []
mate = []

boardimg = pygame.image.load('images/ChessBoardTile.png')   # Tabuleiro
yellowtile = pygame.image.load('images/YellowTile.png')     # Tile amarela
greentile = pygame.image.load('images/GreenTile.png')       # Tile verde
redtile = pygame.image.load('images/RedTile.png')           # Tile vermelha

# Peças
peaow = pygame.image.load('images/PeaoW.png')
peaob = pygame.image.load('images/PeaoB.png')
torrew = pygame.image.load('images/TorreW.png')
torreb = pygame.image.load('images/TorreB.png')
horsew = pygame.image.load('images/HorseW.png')
horseb = pygame.image.load('images/HorseB.png')
bispow = pygame.image.load('images/BispoW.png')
bispob = pygame.image.load('images/BispoB.png')
queenw = pygame.image.load('images/QueenW.png')
queenb = pygame.image.load('images/QueenB.png')
reiw = pygame.image.load('images/ReiW.png')
reib = pygame.image.load('images/ReiB.png')

# Moldura
frame = pygame.image.load('images/Frame.png')
sideframe = pygame.image.load('images/SideFrame.png')

# fonte
myfont = pygame.font.SysFont('Comic Sans MS', 20)

# Superfície de tempo
timer = pygame.time.get_ticks()/1000
timersurface = myfont.render(f'{int(timer)}', False, (0, 0, 0))

# Telas de fim
whitewon = pygame.image.load('images/WhiteWon.png')
blackwon = pygame.image.load('images/BlackWon.png')


def setonscreen(screen):    # Colocar na tela
    # print('setonscreen')
    global board
    screen.blit(frame, (0, 0))              # Moldura
    screen.blit(boardimg, (16, 16))         # Tabuleiro
    board = BoardManager.getboard()
    if s := BoardManager.getselected():     # Movetiles
        screen.blit(yellowtile, ((s[0] * 75)+16, (s[1] * 75)+16))
        movelist = BoardManager.getmovelist()
        smashlist = BoardManager.getsmashlist()
        for v in movelist:
            screen.blit(greentile, ((v[0]*75)+16, (v[1]*75)+16))
        for v in smashlist:
            screen.blit(redtile, ((v[0] * 75)+16, (v[1] * 75)+16))
    for k, v in enumerate(board):           # Peças
        for k1, v1 in enumerate(v):
            x = (k * 75) + 16
            y = (k1 * 75) + 16
            if int(v1) == -1:
                screen.blit(peaow, (x, y))
            elif int(v1) == 1:
                screen.blit(peaob, (x, y))
            elif int(v1) == -2:
                screen.blit(torrew, (x, y))
            elif int(v1) == 2:
                screen.blit(torreb, (x, y))
            elif int(v1) == -3:
                screen.blit(horsew, (x, y))
            elif int(v1) == 3:
                screen.blit(horseb, (x, y))
            elif int(v1) == -4:
                screen.blit(bispow, (x, y))
            elif int(v1) == 4:
                screen.blit(bispob, (x, y))
            elif int(v1) == -5:
                screen.blit(queenw, (x, y))
            elif int(v1) == 5:
                screen.blit(queenb, (x, y))
            elif int(v1) == -6:
                screen.blit(reiw, (x, y))
            elif int(v1) == 6:
                screen.blit(reib, (x, y))


def getmate():
    global mate
    mate = BoardManager.getmate()
    return mate


def endscreen(p, screen):
    if p:
        screen.blit(blackwon, (0, 0))
    else:
        screen.blit(whitewon, (0, 0))


def timeronscreen(screen):
    global timer, timersurface
    screen.blit(sideframe, (632, 0))
    timer = pygame.time.get_ticks() / 1000
    timersurface = myfont.render(f'{int(timer)}', False, (0, 0, 0))
    screen.blit(timersurface, (682, 0))


def update():   # Atuliza no looping
    # print('update screen')
    BoardManager.update()


