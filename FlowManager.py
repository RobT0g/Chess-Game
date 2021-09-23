import AnalyseTools


board = []                  # Provavelmente inútil
globalmove = {}
ktile = [[], []]            # Posição dos reis
wcheck = bcheck = False     # Check da peças
ktreats = []


def initialize(boar):   # Inicia ou atualiza a variável de posições interna
    global board, ktile
    board = boar
    ktile = [[4, 7], [4, 0]]


def upkingpos(p, x, y):        # Atualiza a posição atual dos reis
    global ktile
    if p == -6:
        ktile[0] = [x, y]
    elif p == 6:
        ktile[1] = [x, y]


def getkingpos():
    global ktile
    return ktile


def setcautking():
    global globalmove, ktreats
    ktreats = [[], []]
    for k, v in globalmove.items():
        if int(float(k)) in range(-1, -7, -1):
            if ktile[1] in v[1]:
                ktreats[1].append(float(k))
        if int(float(k)) in range(1, 7):
            if ktile[0] in v[1]:
                ktreats[0].append(float(k))


def kingstate():
    global ktreats
    return ktreats
    # Isso vai pro MoveManager e vai atuar restringindo o movimento na vez de um jogador


def upgmove(dic):
    global globalmove
    globalmove = dic
    setcautking()
    # AnalyseTools.dichec(globalmove)
