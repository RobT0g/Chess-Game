import InputManager
import MoveManager
import pygame
from pygame.locals import *


pygame.init()               # Inicialização
board = []                  # Variável de posições de peças
sxy = []
pos = []
movelist = []
smashlist = []
wturn = True
mate = []

for i in range(0, 8):
    board.append([])
    for j in range(0, 8):
        board[i].append(0.0)


def alinitpos():
    global board
    for i in range(0, 8):
        board[i][1] = (11+i)/10
    for i in range(0, 3):
        board[i][0] = 2.1 + i
    board[3][0] = 5.0
    board[4][0] = 6.0
    board[5][0] = 4.2
    board[6][0] = 3.2
    board[7][0] = 2.2
    for v in board:
        v[7] = -v[0]
        v[6] = -v[1]


def initialize():                       # Posições iniciais
    alinitpos()
    MoveManager.initialize(board)


def upboard(p, x, y, x0, y0):   # Atualiza a variável de posições interna
    # print('Update board position')
    global board
    board[x][y] = p
    board[x0][y0] = 0.0


def getboard():
    global board
    return board


def update():       # Atualiza a cada clickada
    global board, mate
    MoveManager.update()
    if x := MoveManager.actualmove():
        upboard(x[0], x[1], x[2], x[3], x[4])
        MoveManager.upboard(board)
        MoveManager.upgmove(x[0], x[1], x[2])
        mate = MoveManager.matecheck()


def getmate():
    global mate
    return mate


def getselected():  # Retorna a peça selecionada
    global sxy
    sxy = MoveManager.getseltile()
    if sxy:
        return sxy
    else:
        return sxy


def getmovelist():      # Retorna as posições pra onde a peça selecionada pode se mover
    global movelist
    movelist = MoveManager.getmovelist()
    return movelist


def getsmashlist():     # Retorna as posições em que uma peça pode comer outra
    global smashlist
    smashlist = MoveManager.getsmashlist()
    return smashlist
