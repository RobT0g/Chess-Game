def dichec(dic):
    while (x := input('Peça: ')) != '69':
        print('-'*30)
        if x in dic.keys():
            print('-'*30)
            print(f'    Move list: {dic[x][0]}')
            print(f'    Smash list: {dic[x][1]}')
            print('-'*30)
        elif x == 'keys':
            print(dic.keys())
        else:
            print('Nao tem essa peça')
