DEBUG = True

def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)



def print_board(board):
    rown = 1
    #print("  ", end="")
    #print("__ "*8)
    for row in board:
        print(str(rown)+" ", end="")
        rown += 1
        for c in row:
            #if row.index(c)%2==1:
            print(c, end="")
            #else:
                #print("! "+c+" ", end="")
        print("")
        #print("_ "*8)
    print("  ", end="")
    for i in range(1,9):
        print(str(i), end="")
    print("")

white_p = ['\u2659','\u2659','\u2659','\u2659','\u2659','\u2659','\u2659','\u2659','\u2656','\u2658','\u2657','\u2655','\u2654','\u2657','\u2658','\u2656']
black_p = ['\u265C','\u265E','\u265D','\u265B','\u265A','\u265D','\u265E','\u265C','\u265F','\u265F','\u265F','\u265F','\u265F','\u265F','\u265F','\u265F']

def new_board():
    board = [['□'] *8 for i in range(8)]
    board[0] = ['♜','♞','♝','♛','♚','♝','♞','♜']
    board[1] = ['♟','♟','♟','♟','♟','♟','♟','♟']
    board[6] = ['♙','♙','♙','♙','♙','♙','♙','♙']
    board[7] = ['♖','♘','♗','♕','♔','♗','♘','♖']
    return board

def read_step():
    piece_choice = [int(i)-1 for i in input().split()]
    piece_step = [int(i)- 1 for i in input().split()]
    return piece_choice, piece_step

def check_step(s,b,order):
    piece_choice = s[0]
    piece_step = s[1] 
    chosen = b[piece_choice[0]][piece_choice[1]]
    chosen_step = b[piece_step[0]][piece_step[1]]
    order_p = white_p if order == "white" else black_p
    log(chosen)
    if chosen not in order_p:
        log("wrong chosen")
        return False
    if chosen_step != "□" and chosen_step in order_p:
        log("wrong victim")
        return False
    if chosen in ["♙", '♟']:
        log("checking pawn")
        if chosen_step=='□' :
            if (piece_choice[0]==6 or piece_choice[0]==1) and (piece_step[0]==piece_choice[0]+2 if order=="black" else piece_step[0]==piece_choice[0]-2):
                return True
            if piece_step[0]==piece_choice[0]+1 if order=="black" else piece_step[0]==piece_choice[0]-1:
                return True  
            else:
                return False
        else:
            # Нужно сделать ан пассант
            if (piece_choice[1]+1==piece_step[1] or piece_choice[1]-1==piece_step[1]) and piece_choice[0]+1==piece_step[0] if order=="black" else piece_choice[0]-1==piece_step[0]:
                return True
            else:
                return False
    if chosen == "♖" or '♜':
        log("checking tower")
        if piece_choice[1] == piece_step[1] or piece_choice[0] == piece_step[0] and collision(b,piece_choice,piece_step):
            return True
        else:
            return False
    if chosen == "♘" or '♞':
        log("checking knight")
        d = (abs(piece_choice[0]-piece_step[0]), abs(piece_choice[1]-piece_step[1]))
        log(d)
        if d == (1, 2) or d == (2, 1):
            return True
        return False
    if chosen == "♗" or '♝':
        log("checking bishop")
        if abs(piece_choice[1]-piece_step[1]) == abs(piece_choice[0]-piece_step[0]) and collision(b,piece_choice,piece_step):
            return True
        else:
            return False
    if chosen == "♕" or '♛':
        log("checking queen") 
        if (piece_choice[1]-piece_step[1]) == abs(piece_choice[0]-piece_step[0]) or (piece_choice[1]==piece_step[1])or(piece_choice[0]==piece_step[0]) and collision(b,piece_choice,piece_step):
            return True
        else:
            return False
    if chosen == "♔" or '♚':
        log("checking king")
        if abs(piece_choice[1]-piece_step[1]) <= 1 and abs(piece_choice[0]-piece_step[0]) <= 1:
            return True
        else:
            return False
def collision(b, f, t): # true - путь свободен, false - на пути преграда
    dy = t[0] - f[0]
    dx = t[1] - f[1]
    y = 0 if dy == 0 else dy/abs(dy)
    x = 0 if dx == 0 else dx/abs(dx)
    while True:
        f = (f[0]+y, f[1]+x)
        if f == t:
            break
        if b[y][x] != "□":
            return False
    return True


def apply_step(b,s):
    global def_pieces
    piece_choice = s[0]
    piece_step = s[1] 
    b[piece_step[0]][piece_step[1]] = b[piece_choice[0]][piece_choice[1]]
    def_pieces.append(b[piece_step[0]][piece_step[1]])
    #print(b)
    b[piece_choice[0]][piece_choice[1]] = '□'
    #b[6][0] = "♙"
    return b
#def check(b,order): 
 #   arr_atack = []
  #  for i in b:
   #     for j in i:
    #        if order =='white':
     #           wh=i.index("♔")
      #      else:
       #         bl=b.index("♚")
        #    if i.index()
#
 #   if a in arr_atack:
  #      print True

    #if 
    return False
def swip_order(order):
    return "black" if order == "white" else "white"

#check_step(read_step())

#print(print_board(new_board()), swip_order("white"))

#def check_step()
def_pieces= []
board = new_board()
order = "white" # or black
while True:
    if not DEBUG:
        print("\033c")
    print_board(board)
    print(order)
    step = read_step()
    correctness = check_step(step, board, order)
    log("correct step" if correctness else "wrong step")
    if correctness:
        #print(check_step) 
        board = apply_step(board, step)
        log(board)
        order = swip_order(order)
    #if check(board,order):
     #   print(order+" king in danger")
    if '♚' in def_pieces or "♔" in def_pieces:
        break

#Создать проверку на то какого цвета фигура
#Создать функции для:
#Создания поля нулевого хода
#Отрисовки каждого нового хода
#Чтения хода, считывающее координаты из инпутп и возвращающий массив с ходом
#Проверки хода на допустимость, в качестве аргументов берутся: массив с ходом, текущее состояние доски и очередь. Возврашает True или False
#Выполнения хода
#Проверки на Мат
#Смены хода 

#Нужно сделать историю ходов или хотя бы переменную с предыдущим ходом
#Нужно сделать вывод ошибки при неправильном ходе
#Нужно сделать проверку на то есть ли на пути фигуры другая фигура
#Нужно сделать переход пешки в другую фигуру при достижении противоположного конца поля
