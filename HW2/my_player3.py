from copy import deepcopy

#inspirtion from host.py
def detect_neighbor(i, j):
    neighbors = []
    coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    neighbors = [(i+c[0],j+c[1]) for c in coordinates if (0<=j+c[1]<5 and 0<=i+c[0]<5)]
    return neighbors

def chain_stones(i, j, board, my_colour):
    stack = [(i, j)]  
    visited = {}
    visited[(i,j)]=True
    chain = []  
    while stack:
        cur = stack.pop()
        chain.append(cur)
        for n in detect_neighbor(cur[0], cur[1]):
            if board[n[0]][n[1]] == my_colour:  
                if n not in visited:
                    stack.append(n)
                    visited[n]=True
    return chain


def has_liberty(i, j, board, my_colour):
    for stone in chain_stones(i, j, board, my_colour):
        for n in detect_neighbor(stone[0], stone[1]):
            if board[n[0]][n[1]] == 0:
                return True
    return False


def stones_died(my_colour, board):
    dead = []
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == my_colour:
                if not has_liberty(i, j, board, my_colour):
                    dead.append((i, j))
    return dead


def liberty_positions(i,j,board,my_colour):
    liberties=set()
    for stone in chain_stones(i,j,board,my_colour):
        for n in detect_neighbor(stone[0], stone[1]):
            if board[n[0]][n[1]] == 0:
                liberties.add(n)
    return liberties
    
def trial(i, j, board, my_colour):
    temp = deepcopy(board)
    temp[i][j] = my_colour
    opponent_dead_stones = stones_died(3-my_colour, temp)
    for stone in opponent_dead_stones:
        temp[stone[0]][stone[1]] = 0
    my_dead_stones = stones_died(my_colour, temp)
    for stone in my_dead_stones:
        temp[stone[0]][stone[1]] = 0
    return temp,len(my_dead_stones),len(opponent_dead_stones)

def utility_value(board,my_colour):
    black_stones = -3
    white_stones = 3
    black_in_danger=0
    white_in_danger=0
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == 1:
                lib_count = len(liberty_positions(i,j,board,1))
                if lib_count<=1:
                    black_in_danger+=1
                black_stones += 1
            elif board[i][j] == 2:
                lib_count = len(liberty_positions(i,j,board,2))
                if lib_count<=1:
                    white_in_danger+=1
                white_stones += 1
    if my_colour==1: #black utility value 
        util_val = (10*black_stones)-(10*white_stones)+(2*white_in_danger)-(1.5*black_in_danger)
    else: #white utility value
        util_val = (10*white_stones)-(10*black_stones)+(2*black_in_danger)-(1.5*white_in_danger)
    return util_val

def safe_moves(my_colour, prev_board, cur_board):
    all_moves=set()
    safe = []
    for i in range(0, 5):
        for j in range(0, 5):
            if cur_board[i][j]!=0:
                all_moves|=liberty_positions(i,j,cur_board,cur_board[i][j])
    for pos in all_moves:
        board_after_move,my_dead_stones,opponent_dead_stones = trial(pos[0],pos[1],cur_board,my_colour)
        if board_after_move != cur_board and board_after_move != prev_board: #suicide move and KO move check
            safe.append((pos[0], pos[1],opponent_dead_stones-my_dead_stones)) 
    if len(safe)!= 0:   
        return sorted(safe, key=lambda x:-x[2])
    return None

def maximizer(cur_board,prev_board,my_colour,depth,alpha,beta):
    if depth == 0:
        value = utility_value(cur_board,my_colour)
        return value,[]
    opponent_stones = 0
    my_stones = 0
    for i in range(5):
        for j in range(5):
            if cur_board[i][j]==3-my_colour:
                opponent_stones+=1
            if cur_board[i][j]==my_colour:
                my_stones+=1
    if opponent_stones==0 and my_stones==0:
        return 100,[(2,2)]
    if opponent_stones==1 and my_stones==0:
        if cur_board[2][2]==3-my_colour:
            return 100,[(2,1)]
        else:
            return 100,[(2,2)]
    my_moves = safe_moves(my_colour, prev_board, cur_board)
    max_value = float('-inf')
    max_value_action = []
    for move in my_moves:
        temp = deepcopy(cur_board)
        next_board,my_dead_stones,opponent_dead_stones = trial(move[0],move[1],temp, my_colour)
        value, actions = minimizer(next_board,cur_board,3-my_colour,depth-1,alpha,beta)
        value+= (opponent_dead_stones*5) - (my_dead_stones*8.5)
        if value > max_value:
            max_value = value
            max_value_action = [move]+actions
        if max_value >= beta: #prune
            return max_value, max_value_action
        if max_value > alpha:
            alpha = max_value
    return max_value, max_value_action    
    
def minimizer(cur_board,prev_board,my_colour,depth,alpha,beta):
    if depth == 0:
        value = utility_value(cur_board,my_colour)
        return value,[]
    min_value = float('inf')
    opponent_stones = 0
    my_stones = 0
    for i in range(5):
        for j in range(5):
            if cur_board[i][j]==3-my_colour:
                opponent_stones+=1
            if cur_board[i][j]==my_colour:
                my_stones+=1
    if opponent_stones==0 and my_stones==0:
        return 100,[(2,2)]
    if opponent_stones==1 and my_stones==0:
        if cur_board[2][2]==3-my_colour:
            return 100,[(2,1)]
        else:
            return 100,[(2,2)]
    my_moves = safe_moves(my_colour, prev_board, cur_board)
    min_value_action = []
    for move in my_moves:
        temp = deepcopy(cur_board)
        next_board,my_dead_stones,opponent_dead_stones = trial(move[0], move[1], temp, my_colour)
        value, actions = maximizer(next_board,cur_board,3-my_colour,depth-1, alpha, beta)
        value+= (opponent_dead_stones*5) - (my_dead_stones*8.5)
        if value < min_value:
            min_value = value
            min_value_action = [move]+actions
        if min_value <= alpha: #prune
            return min_value, min_value_action
        if min_value < beta:
            alpha = min_value
    return min_value,min_value_action


def best_move(cur_board,prev_board,my_colour,depth):
    score, actions = maximizer(cur_board,prev_board,my_colour,depth,float("-inf"),float("inf"))
    if len(actions) > 0:
        return actions[0] 
    else:
        return "PASS"


with open('input.txt', 'r') as f:
    lines = f.read()
lines = lines.split('\n')
my_colour = int(lines[0])
prev_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:6]]
cur_board = [[int(x) for x in line.rstrip('\n')] for line in lines[6:11]]
depth=4
action = best_move(cur_board,prev_board,my_colour,depth)
f = open("output.txt", "w")
if action != "PASS":
    f.write(str(action[0]) + ',' + str(action[1]))
else:
    f.write("PASS")
f.close()