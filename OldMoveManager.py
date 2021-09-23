import InputManager
import FlowManager
import AnalyseTools


board = []
sxy = []
pos = []
movelist = []
smashlist = []
ktreats = [[], []]
globalmove = {}
wturn = True
justmoved = False


def update():
    print('update move')
    global board, sxy, ktreats, wturn, globalmove, movelist
    selpiece()
    if sxy:
        if (p := board[sxy[0]][sxy[1]]) not in (6, -6):
            if wturn and ktreats[0]:
                oncheckmoves(int(p), sxy[0], sxy[1])
            elif not wturn and ktreats[1]:
                oncheckmoves(int(p), sxy[0], sxy[1])
            else:
                setmovelist(int(p), sxy[0], sxy[1])
        else:
            setmovelist(int(p), sxy[0], sxy[1])
            instml = movelist[:]
            movelist = []
            instdel = []
            if p == -6:
                for k, v in globalmove.items():
                    if int(float(k)) in range(1, 7):
                        for k1, v1 in enumerate(instml):
                            if v1 in v[0]:
                                instdel.append(k1)
            elif p == 6:
                for k, v in globalmove.items():
                    if int(float(k)) in range(-1, -7, -1):
                        for k1, v1 in enumerate(instml):
                            if v1 in v[0]:
                                instdel.append(k1)
            if instml and instdel:
                for k, v in instml:
                    if k not in instdel:
                        print('')
                        # movelist.append(v)


def initialize(boar):       # Inicializa a variável interna de posições
    print('initilize move')
    global board, globalmove
    board = boar
    FlowManager.initialize(board)
    currentgmv()


def currentgmv(test=False):
    print('current global move')
    global globalmove, movelist, smashlist, board
    instidck = []
    delpieces = []
    for k, v in enumerate(board):
        for k1, v1 in enumerate(v):
            if v1 != 0:
                instidck.append(v1)
                setmovelist(int(v1), k, k1)
                globalmove[str(v1)] = [movelist, smashlist]
    for k in globalmove.keys():
        if (x := float(k)) not in instidck:
            delpieces.append(k)
    if delpieces:
        del globalmove[delpieces[0]]


def selpiece():             # Redefine a peça selecionada
    print('selpiece move')
    global sxy, wturn
    if InputManager.clickable():
        uppos()
        if wturn and iswhite() and (int(board[pos[0]][pos[1]]) in range(-1, -7, -1)):
            sxy = pos[:]
        elif (not wturn) and (not iswhite()) and (int(board[pos[0]][pos[1]]) in range(1, 7)):
            sxy = pos[:]


def uppos():        # Redefine a posição do mouse em relação do tabuleiro
    print('uppos move')
    global pos
    pos = InputManager.secl()


def iswhite(x=-9, y=-9):
    global pos, board
    if x == -9 and y == -9:     # Informa se a peça sob o meuse é branca
        if int(board[pos[0]][pos[1]]) in range(-1, -7, -1):
            return True
        elif int(board[pos[0]][pos[1]]) in range(1, 7):
            return False
    else:
        if int(board[x][y]) in range(-1, -7, -1):    # Informa se a peça na posição dita é branca
            return True
        elif int(board[x][y]) in range(1, 7):
            return False


def setmovelist(p, x, y):       # Redefine a listas de movimento e comer
    print('setmovelist')
    global movelist, smashlist, board
    movelist = []
    smashlist = []
    instml = []
    if p in (1, -1):  # Peão
        instml = [[[x, y + p]]]
        if iswhite(x, y) and y == 6:
            instml[0].append([x, y + (2 * p)])
        elif (not iswhite(x, y)) and y == 1:
            instml[0].append([x, y + (2 * p)])
        if p == -1:
            if x + 1 in range(0, 8) and y - 1 in range(0, 8):
                if board[x + 1][y - 1] > 1:
                    smashlist.append([x + 1, y - 1])
            if x - 1 in range(0, 8) and y - 1 in range(0, 8):
                if board[x - 1][y - 1] > 1:
                    smashlist.append([x - 1, y - 1])
        elif p == 1:
            if x + 1 in range(0, 8) and y + 1 in range(0, 8):
                if board[x + 1][y + 1] < -1:
                    smashlist.append([x + 1, y + 1])
            if x - 1 in range(0, 8) and y + 1 in range(0, 8):
                if board[x - 1][y + 1] < -1:
                    smashlist.append([x - 1, y + 1])
        # Adicionar condição de fim do tabuleiro
    elif p in (2, -2):  # Torre
        instml = [[], [], [], []]
        for i in contagem(x + 1, 7):
            instml[0].append([i, y])
        for i in contagem(x - 1, 0):
            instml[1].append([i, y])
        for i in contagem(y + 1, 7):
            instml[2].append([x, i])
        for i in contagem(y - 1, 0):
            instml[3].append([x, i])
    elif p in (3, -3):  # Cavalo
        instml = [[[x + 2, y + 1], [x + 2, y - 1], [x - 2, y + 1], [x - 2, y - 1],
                   [x + 1, y + 2], [x + 1, y - 2], [x - 1, y + 2], [x - 1, y - 2]]]
    elif p in (4, -4):  # Bispo
        instml = [[], [], [], []]
        for i in contagem(1, 7 - x):
            instml[0].append([x + i, y + i])
            instml[1].append([x + i, y - i])
        for i in contagem(1, x):
            instml[2].append([x - i, y + i])
            instml[3].append([x - i, y - i])
    elif p in (5, -5):  # Rainha
        instml = [[], [], [], [], [], [], [], []]
        for i in contagem(x + 1, 7):
            instml[0].append([i, y])
        for i in contagem(x - 1, 0):
            instml[1].append([i, y])
        for i in contagem(y + 1, 7):
            instml[2].append([x, i])
        for i in contagem(y - 1, 0):
            instml[3].append([x, i])
        for i in contagem(1, 7 - x):
            instml[4].append([x + i, y + i])
            instml[5].append([x + i, y - i])
        for i in contagem(1, x):
            instml[6].append([x - i, y + i])
            instml[7].append([x - i, y - i])
    elif p in (6, -6):
        instml = [[[x + 1, y], [x + 1, y + 1], [x, y + 1], [x - 1, y + 1],
                   [x - 1, y], [x - 1, y - 1], [x, y - 1], [x + 1, y - 1]]]
    for v1 in instml:  # Testar casas livres dentro dos movimentos
        for v in v1:
            if (v[0] in range(0, 8)) and (v[1] in range(0, 8)) and (p not in (3, -3, 6, -6)):  # N rei ou cavalo
                if board[v[0]][v[1]] == 0:
                    movelist.append([v[0], v[1]])
                else:
                    if (p not in (1, -1)) and (iswhite(x, y)) and (board[v[0]][v[1]] >= 1):
                        smashlist.append([v[0], v[1]])
                    elif (p not in (1, -1)) and (not iswhite(x, y)) and (board[v[0]][v[1]] <= -1):
                        smashlist.append([v[0], v[1]])
                    break
            elif p in (3, -3, 6, -6):
                if (v[0] in range(0, 8)) and (v[1] in range(0, 8)):
                    if board[v[0]][v[1]] == 0:
                        movelist.append([v[0], v[1]])
                    elif (iswhite(x, y)) and board[v[0]][v[1]] > 1:
                        smashlist.append([v[0], v[1]])
                    elif (not iswhite(x, y)) and board[v[0]][v[1]] < -1:
                        smashlist.append([v[0], v[1]])
            else:
                break


def oncheckmoves(p, x, y):  # Filtro de movimentos em caso de rei em check
    print('oncheckmoves')
    global ktreats, board, movelist, smashlist, globalmove, sxy
    if wturn and ktreats[0]:    # Rei branco em check e vez do braco
        setmovelist(p, x, y)    # Atualiza as lista de movimentos
        instml = movelist[:]    # Movimentos inst
        instsl = smashlist[:]   # Ataques inst
        instdel = []            # Lista de deleções
        for k, v in enumerate(instml):      # Teste dos movimentos
            board[v[0]][v[1]] = p
            board[x][y] = 0.0
            currentgmv()
            FlowManager.upkingpos(p, v[0], v[1])
            FlowManager.upgmove(globalmove)
            if FlowManager.kingstate()[0]:  # Informa pro instdel cada movimento que não desfaz o check
                instdel.append(k)
            board[v[0]][v[1]] = 0.0
            board[x][y] = p
        movelist = []                       # Reseta a movelist
        if instml and instdel:
            for k, v in enumerate(instml):
                if k not in instdel:        # Insere os movimentos que desfazem o check na movelist
                    movelist.append(v)
        elif instml:
            movelist = instml[:]
        instdel = []                        # Reseta o instdel pra reuso
        for k, v in enumerate(instsl):      # Teste dos ataques
            aux = board[v[0]][v[1]]
            board[v[0]][v[1]] = p
            board[x][y] = 0.0
            currentgmv()
            FlowManager.upkingpos(p, v[0], v[1])
            FlowManager.upgmove(globalmove)
            if FlowManager.kingstate()[0]:
                instdel.append(k)
            board[v[0]][v[1]] = aux
            board[x][y] = p
        if instsl and instdel:
            smashlist = []
            for k, v in enumerate(instsl):
                if k not in instdel:
                    smashlist.append(v)
        else:
            smashlist = instsl[:]
    elif not wturn and ktreats[1]:
        setmovelist(p, x, y)
        instml = movelist[:]
        instsl = smashlist[:]
        instdel = []
        for k, v in enumerate(instml):
            board[v[0]][v[1]] = p
            board[x][y] = 0.0
            currentgmv()
            FlowManager.upkingpos(p, v[0], v[1])
            FlowManager.upgmove(globalmove)
            if FlowManager.kingstate()[1]:
                instdel.append(k)
            board[v[0]][v[1]] = 0.0
            board[x][y] = p
        movelist = []
        if instml and instdel:
            for k, v in enumerate(instml):
                if k not in instdel:
                    movelist.append(v)
        elif instml:
            movelist = instml[:]
        instdel = []
        for k, v in enumerate(instsl):
            aux = board[v[0]][v[1]]
            board[v[0]][v[1]] = p
            board[x][y] = 0.0
            currentgmv()
            FlowManager.upkingpos(p, v[0], v[1])
            FlowManager.upgmove(globalmove)
            if FlowManager.kingstate()[1]:
                instdel.append(k)
            board[v[0]][v[1]] = aux
            board[x][y] = p
        if instsl and instdel:
            smashlist = []
            for k, v in enumerate(instsl):
                if k not in instdel:
                    smashlist.append(v)
        else:
            smashlist = instsl[:]
    else:
        print('Erro')
    # Inconsistência no filtro da smashlist


def getmovelist():      # Retorna a lista de movimento
    print('getmovelist move')
    global movelist
    return movelist


def getsmashlist():     # Retorna a lista de peças que pode comer
    print('getsmashlist')
    global smashlist
    return smashlist


def contagem(a, b):     # Contagem dependente da ordem
    c = []
    if a < b:
        for i in range(a, b + 1):
            c.append(i)
    else:
        for i in range(a, b - 1, -1):
            c.append(i)
    return c[:]


def getseltile():   # Retorna a posição da peça selecionada
    print('getseltile move')
    global sxy
    return sxy


def actualmove():       # Retorna uma lista de posições quanto ao movimento da peça selecionada
    global movelist, sxy, wturn
    uppos()
    if sxy and ((pos in movelist) or (pos in smashlist)):
        aux = [board[sxy[0]][sxy[1]], pos[0], pos[1], sxy[0], sxy[1]][:]
        sxy = []
        wturn = not wturn
        return aux


def upboard(boar):      # Atualiza a variável de teclado interno
    print('upboard')
    global board
    board = boar
    FlowManager.initialize(board)


def upgmove(p, x, y):
    global globalmove, ktreats
    currentgmv()
    # AnalyseTools.dichec(globalmove)
    FlowManager.upkingpos(p, x, y)
    FlowManager.upgmove(globalmove)
    ktreats = FlowManager.kingstate()
