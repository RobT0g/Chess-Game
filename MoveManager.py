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
nowayout = [False, False]


def initialize(boar):
    global board, globalmove
    board = boar
    FlowManager.initialize(board)
    currentgmv()


def update():
    selpiece()


def selpiece():
    global sxy, wturn
    if InputManager.clickable():
        uppos()
        if wturn and iswhite() and (int(board[pos[0]][pos[1]]) in range(-1, -7, -1)):
            sxy = pos[:]
        elif (not wturn) and (not iswhite()) and (int(board[pos[0]][pos[1]]) in range(1, 7)):
            sxy = pos[:]


def getseltile():
    global sxy
    return sxy


def uppos():
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


def oncheckmoves(p, x, y):                      # Filtro dos movimentos quando em check
    # p: peça(float), x e y: posição da peça analisada
    global board, movelist, smashlist
    instml = globalmove[str(p)][0][:]           # Movimentos inst
    instsl = globalmove[str(p)][1][:]           # Ataques inst
    insgmoves = {}                              # Movimentos globais de verificação
    movelist = []
    smashlist = []
    instdel = []                                # Movimentos a serem apagados
    # Aqui vai ser analisado se algum movimento deve ser apagado
    for k, v in enumerate(instml):
        board[v[0]][v[1]] = p
        board[x][y] = 0.0
        insgmoves = currentgmv(True)
        FlowManager.upkingpos(p, v[0], v[1])
        FlowManager.upgmove(insgmoves)
        kt = FlowManager.kingstate()
        if ((p <= -1) and kt[0]) or ((p >= -1) and kt[1]):      # Filtro de mistura
            instdel.append(k)
        board[v[0]][v[1]] = 0.0
        board[x][y] = p
        FlowManager.upkingpos(p, x, y)
        FlowManager.upgmove(globalmove)
    if instml and instdel:                      # Confere se há algum movimento pra apagar
        for k, v in enumerate(instml):
            if k not in instdel:                # Insere os movimentos que desfazem o check na movelist
                movelist.append(v)
    elif instml:                                # Caso não aja movimentos pra apagar, a movelist é a default
        movelist = instml[:]
    instdel = []
    # Aqui vai ser analisado se algum ataque deve ser apagado
    for k, v in enumerate(instsl):
        aux = board[v[0]][v[1]]
        board[v[0]][v[1]] = p
        board[x][y] = 0.0
        insgmoves = currentgmv(True)
        FlowManager.upkingpos(p, v[0], v[1])
        FlowManager.upgmove(insgmoves)
        kt = FlowManager.kingstate()
        if ((p <= -1) and kt[0]) or ((p >= -1) and kt[1]):      # Filtro de mistura
            instdel.append(k)
        board[v[0]][v[1]] = aux
        board[x][y] = p
        FlowManager.upkingpos(p, x, y)
        FlowManager.upgmove(globalmove)
    if instsl and instdel:                      # Confere se há algum ataque pra apagar
        for k, v in enumerate(instsl):
            if k not in instdel:                # Insere os ataques que desfazem o check na movelist
                smashlist.append(v)
    elif instsl:                                # Caso não aja ataques pra apagar, a smashlist é a default
        smashlist = instsl[:]


def normalmoves(p, x, y):
    global movelist, smashlist, board
    movelist = []
    smashlist = []
    instml = []                         # Movimentos não filtrados
    # Dentro da lista acima vão ter outras listas, cada demonstrando os movimentos da peça em uma determinda direção.
    # O looping do filtro testa as direcões independentemente para impedir caso a movimentação até o fim seja impedida
    # por uma peça no meio. Cada direção é uma "Progressão".
    if p in (1, -1):    # Movimentos do peão
        instml = [[[x, y+p]]]                   # 1 casa à frente
        if ((p == 1) and (y == 1)) or ((p == -1) and (y == 6)):
            instml[0].append([x, y+(2*p)])      # 2 casas se tiver no default
        # Smashlist
        if (x + 1 in range(0, 8)) and (y + p in range(0, 8)):
            if smashable(p, x+1, y+p):          # Diagonal à direita
                smashlist.append([x + 1, y + p])
        if (x - 1 in range(0, 8)) and (y + p in range(0, 8)):
            if smashable(p, x-1, y+p):          # Diagonal à esquerda
                smashlist.append([x - 1, y + p])
    elif p in (2, -2):                  # Movimentos da Torre
        instml = [[], [], [], []]       # 4 Progressões
        for i in contagem(x + 1, 7):    # Movimentos em +x
            instml[0].append([i, y])
        for i in contagem(x - 1, 0):    # Movimentos em -x
            instml[1].append([i, y])
        for i in contagem(y + 1, 7):    # Movimentos em +y
            instml[2].append([x, i])
        for i in contagem(y - 1, 0):    # Movimentos em -y
            instml[3].append([x, i])
    elif p in (3, -3):  # Movimentos do cavalo
        instml = [[[x + 2, y + 1]], [[x + 2, y - 1]], [[x - 2, y + 1]], [[x - 2, y - 1]],   # Sem progressão
                  [[x + 1, y + 2]], [[x + 1, y - 2]], [[x - 1, y + 2]], [[x - 1, y - 2]]]
    elif p in (4, -4):  # Movimentos do bispo
        instml = [[], [], [], []]               # 4 Progressões
        for i in contagem(1, 7 - x):
            instml[0].append([x + i, y + i])    # +x+y
            instml[1].append([x + i, y - i])    # +x-y
        for i in contagem(1, x):
            instml[2].append([x - i, y + i])    # -x+y
            instml[3].append([x - i, y - i])    # -x-y
    elif p in (5, -5):  # Movimentos da rainha
        instml = [[], [], [], [], [], [], [], []]   # 8 Progressões
        # Cópia dos movimentos da torre
        for i in contagem(x + 1, 7):
            instml[0].append([i, y])
        for i in contagem(x - 1, 0):
            instml[1].append([i, y])
        for i in contagem(y + 1, 7):
            instml[2].append([x, i])
        for i in contagem(y - 1, 0):
            instml[3].append([x, i])
        # Cópia dos movimentos
        for i in contagem(1, 7 - x):
            instml[4].append([x + i, y + i])
            instml[5].append([x + i, y - i])
        for i in contagem(1, x):
            instml[6].append([x - i, y + i])
            instml[7].append([x - i, y - i])
    elif p in (6, -6):
        instml = [[[x + 1, y]], [[x + 1, y + 1]], [[x, y + 1]], [[x - 1, y + 1]],
                  [[x - 1, y]], [[x - 1, y - 1]], [[x, y - 1]], [[x + 1, y - 1]]]
    for v1 in instml:   # Filtro de movimentos
        for v in v1:
            if (v[0] in range(0, 8)) and (v[1] in range(0, 8)):
                tile = board[v[0]][v[1]]
                if tile == 0:
                    movelist.append([v[0], v[1]])
                else:
                    # Casa ocupada
                    if p not in (1, -1):
                        if smashable(p, v[0], v[1]):
                            smashlist.append([v[0], v[1]])
                    break
            else:
                # Posição fora do tabuleiro
                break


def kingfilter(instgmoves):
    # Filtro de movimentos do rei
    for p, moves in instgmoves.items():
        movestodel = []
        delmpos = []
        delspos = []
        if float(p) == 6:                           # Porcura os movimentos do rei dentro dos movimentos globais
            for k, v in instgmoves.items():
                if float(k) <= 1:                   # Analisa os movimentos das peças inimigas
                    for v1 in v[0]:                 # Restringe para movimentos, não ataques
                        if (v1 in moves[0]) or (v1 in moves[1]):    # Ativa se o movimento ou ataque do rei coincide
                            movestodel.append(v1)                   # Atualiza a lista de movimentos a apagar
            for md in movestodel:                   # Confere os movimentos a apagar
                if md in instgmoves['6.0'][0]:      # Confere se é movimento
                    delmpos.append(instgmoves['6.0'][0].index(md))
                elif md in instgmoves['6.0'][1]:    # Confere se é ataque
                    delspos.append(instgmoves['6.0'][1].index(md))
            if instgmoves['6.0'][0] and delmpos:    # Se tiver movimento pra apagar
                if len(instgmoves['6.0'][0]) == len(delmpos):
                    instgmoves['6.0'][0] = []
                else:
                    for d in delmpos:
                        del instgmoves['6.0'][0][d]
            if instgmoves['6.0'][1] and delspos:   # Se tiver ataques pra apagar
                if len(instgmoves['6.0'][1]) == len(delmpos):
                    instgmoves['6.0'][1] = []
                else:
                    for d in delspos:
                        del instgmoves['6.0'][1][d]
        elif float(p) == -6:                        # Igual ao de cima, mas pro rei branco
            for k, v in instgmoves.items():
                if float(k) >= 1:
                    for v1 in v[0]:
                        if (v1 in moves[0]) or (v1 in moves[1]):
                            movestodel.append(v1)
                            for md in movestodel:
                                if md in instgmoves['-6.0'][0]:
                                    delmpos.append(instgmoves['-6.0'][0].index(md))
                                elif md in instgmoves['-6.0'][1]:
                                    delspos.append(instgmoves['-6.0'][1].index(md))
                            if delmpos:
                                for d in delmpos:
                                    del instgmoves['-6.0'][0][d]
                            if delspos:
                                for d in delspos:
                                    del instgmoves['-6.0'][0][d]


def currentgmv(nm=False):
    global globalmove, movelist, smashlist, board
    plist = []                          # Lista de peças dentro do board
    delpieces = ''                      # Peça comida no último movimento
    instgmoves = {}
    for k, v in enumerate(board):       # Verifica todas as peças dentro do tabuleiro
        for k1, v1 in enumerate(v):
            if v1 != 0:
                plist.append(v1)                                    # Atualiza a lista de peças
                normalmoves(int(v1), k, k1)                         # Define os movimentos da peça atual
                instgmoves[str(v1)] = [movelist, smashlist]         # Atualiza os movimentos da peça atual no global
    kingfilter(instgmoves)                                          # Filtra os movimentos dos reis
    if nm:
        return instgmoves
    else:
        globalmove = instgmoves.copy()
    for k in globalmove.keys():
        if (x := float(k)) not in plist:    # Verifica se alguma peça foi comida
            delpieces = k                   # Informa a peça que foi coimida
    if delpieces != '':
        del globalmove[delpieces]           # Apaga a peça do registro de movimento global


def globckmoves():
    global globalmove, movelist, smashlist, board
    instgmove = {}
    for k, v in enumerate(board):       # Verifica todas as peças dentro do tabuleiro
        for k1, v1 in enumerate(v):
            if (ktreats[0] and v1 <= 1) or (ktreats[1] and v1 >= 1):    # Condição: Análisa das peças cujo rei está em c
                oncheckmoves(v1, k, k1)                                 # Define os movimentos da peça atual
                instgmove[str(v1)] = [movelist, smashlist]              # Atualiza os movimentos da peça atual no global
    globalmove = instgmove.copy()


def matecheck():
    global globalmove, ktreats, nowayout
    if ktreats[0]:
        for k, v in globalmove.items():
            if float(k) <= 1:
                if v[0] or v[1]:
                    nowayout[0] = False
                    break
                else:
                    nowayout[0] = True
    if ktreats[1]:
        for k, v in globalmove.items():
            if float(k) >= 1:
                if v[0] or v[1]:
                    nowayout[1] = False
                    break
                else:
                    nowayout[1] = True
    return nowayout


def getmovelist():
    global globalmove, board
    p = str(board[sxy[0]][sxy[1]])
    return globalmove[p][0]


def getsmashlist():
    global globalmove, board
    p = str(board[sxy[0]][sxy[1]])
    return globalmove[p][1]


def smashable(p, x1, y1):
    if p > 0:
        if board[x1][y1] < 0:
            return True
    else:
        if board[x1][y1] > 0:
            return True
    return False


def contagem(a, b):     # Contagem dependente da ordem
    c = []
    if a < b:
        for i in range(a, b + 1):
            c.append(i)
    else:
        for i in range(a, b - 1, -1):
            c.append(i)
    return c[:]


def actualmove():
    global globalmove, sxy, wturn, pos
    if sxy:
        p = str(board[sxy[0]][sxy[1]])
        uppos()
        if ([pos[0], pos[1]] in globalmove[p][0]) or ([pos[0], pos[1]] in globalmove[p][1]):
            aux = [board[sxy[0]][sxy[1]], pos[0], pos[1], sxy[0], sxy[1]][:]
            sxy = []
            wturn = not wturn
            return aux


def upboard(boar):      # Atualiza a variável de teclado interno
    global board
    board = boar
    FlowManager.initialize(board)


def upgmove(p, x, y):
    global globalmove, ktreats, nowayout
    currentgmv()
    # AnalyseTools.dichec(globalmove)
    FlowManager.upkingpos(p, x, y)
    FlowManager.upgmove(globalmove)
    ktreats = FlowManager.kingstate()
    if ktreats[0] or ktreats[1]:
        globckmoves()
