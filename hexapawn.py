import copy
from queue import PriorityQueue
import sys

## This function takes four arguments such as the initial state of the board, size of it,
# whether white or black is moving, and the depth of the search.
## This function returns the best choice.
## layers  O         layer 1 
##        /  \
##       O    O      layer 2  etc
def hexapawn(input,size,goal,searchAhead):
    
    start = hexagame(input)
    a = checkWin(start,goal,size)
    if a is True:
        return start
    layer = 1
    nextMoves = generateNew(start,size,goal,"MAX")
    if nextMoves == []:
        return start
    values = []
    for s in nextMoves:
        val = scoreVal(s,size,goal,searchAhead,layer)
        values.append(val)
    insertionSortB(values,nextMoves)
    result = nextMoves[-1]
    strResult = []
    for i in range(size):
        temp = ""
        for j in range(size):
            temp += result[i][j]
        strResult.append(temp)
    return strResult

#MiniMax Alg
##The first layer of states that we need to assign values to is the "next-move" layer
##So hexpawn function will generates all states for next-moves and call find_desire_state to assign value to each of them

##This function generate a score value for the given state and returns the value for the state
##This function returns a value for the state
def scoreVal(start,size,goal,searchAhead,layer):
    a = checkWin(start,goal,size)
    if a != False:
        return a
    result_val = 0
    if layer % 2 == 1:
        mode = "MIN"
    else:
        mode = "MAX"
    new_states = generateNew(start,size,goal,mode)
    if layer >= (searchAhead-1):
        if new_states == []:
            if mode == "MIN":
                return size
            else:
                return -size
        return find_value(new_states,goal,mode,size)
    else:
        values = []
        for x in new_states:
            a = staticEval(x,size,goal,searchAhead,layer+1)
            values.append(rc)
        if new_states == []:
            if mode == "MIN":
                return size
            else:
                return -size
        resultVal = minimax(values,mode)
        return resultVal

## Applies the minimax algorithm and evaluates the position and decides the best move
def minimax(position, searchAhead, alpha, beta, maximizePlayer):
    if searchAhead == 0:
        if (player == "b"):
            return staticEval(start, size, goal, searchAhead, layer)
        else:
            return -1*staticEval(start, size, goal, searchAhead, layer)
    if searchAhead == 1:
        if (player == 'w'):
           return staticEval(start, size, goal, searchAhead, layer)
        else:
            return +1*staticEval(start, size, goal, searchAhead, layer)
  

## returns the minimum value or the maximum value based on MINIMAX level
## This function is takes four agrument: board states in the bottom layer, color of program's pawns, its parents' minimax level, size of board
def find_value(state,goal,modeofparent,size):
    values = []
    if goal == 'w':
        for i in state:
            value = evaluateBoardPieces(i,size)
            values.append(value)
    if goal == 'b':
        for i in state:
            value = evaluateBoardPieces(i,size)
            values.append(value)
    insertionSort(values)
    if modeofparent == "MIN":
        return values[0]
    else:
        return values[-1]   

#Board Evaluator has the three next defs within it
## This function checks is a state is already a winning state
## It returns False when the state have no winner, or returns the winning value if a player wins 
## This function takes three parameters: the state, color of program's pawns, size of board

def checkWin(start,goal,size):
    for i in start[0]:
        if i == 'b':
            if goal == 'b':
                return size
            else:
                return -size
    length = len(start)
    for i in start[length-1]:
        if i == 'w':
            if goal == 'w':
                return size
            else:
                return -size
    return False


## The following two function are evaluation functions
## One of them get called based on the color of program's pawns
## Both of them return a integer for the value of a board state
def evaluateBoardPieces(start,size):
    for i in start[0]:
        if i == 'b':
            return -size
    length = len(start)
    for i in start[length-1]:
        if i == 'w':
            return size
    num_white = 0
    num_black = 0 
    for i in range(size):
        for j in range(size):
            if start[i][j] == 'w':
                num_white += 1
            elif start[i][j] == 'b':
                num_black += 1
    result = num_white - num_black
    result += checkPath(start,size,'w')    
                
    for i in start[0]:
        if i == 'b':
            return size
    length = len(start)
    for i in start[length-1]:
        if i == 'w':
            return -size
    num_white = 0
    num_black = 0 
    for i in range(size):
        for j in range(size):
            if start[i][j] == 'w':
                num_white += 1
            elif start[i][j] == 'b':
                num_black += 1
    result = num_black - num_white
    result += checkPath(start,size,'b')

    return result

## This shows the empty paths that each pawn has that will make them more likely to win
## Then minus the program's number of clear-path-pawn by the opponent's number of clear-path-pawn
## This return a integer value
def checkPath(start,size,mode):
    wScore = 0
    bScore = 0
    result = []
    num_white = 0
    indexs_white = []
    for i in range(size):
        for j in range(size):
            if start[i][j] == "w":
                num_white += 1
                indexs_white.append([i,j])
    for k in indexs_white:
        i = k[0]
        j = k[1]
        index_w = 0
        for x in range(i+1,size):
            if start[x][j] == 'b':
                index_w = 1
            else:
                continue
        if index_w == 0:
            wScore += 1
    num_black = 0
    indexs_black = []
    for i in range(size):
        for j in range(size):
            if start[i][j] == "b":
                num_black += 1
                indexs_black.append([i,j])
    for k in indexs_black:
        i = k[0]
        j = k[1]
        index_b = 0
        for x in range(0,i):
            if start[x][j] == 'w':
                index_b = 1
            else:
                continue
        if index_b == 0:
            bScore += 1
    if mode == 'w':
        result = wScore - bScore
    elif mode == 'b':
        result = bScore - wScore
    return result



#This function returns all possible states for each current player
def generateNew(board,size,player,mode):
    if player == 'w':
        if mode == "MAX":
            return whiteMoves(board,size)
        else:
            return blackMoves(board,size)
    else:
        if mode == "MAX":
            return blackMoves(board,size)
        else:
            return whiteMoves(board,size)
    

## One of them get called based on the color of program's pawns
## they generate new states with the helper function (moveleft, moveup...)
## Both of them return returns a list of states
def whiteMoves(board,size):
    result = []
    num_white = 0
    index_white = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == "w":
                num_white += 1
                index_white.append([i,j])
    for k in index_white:
        i = k[0]
        j = k[1]
        if j >= 1 and i < size-1:
            if board[i+1][j-1] == 'b':
                result.append(move_left_down(board,[i,j]))
        if j < size-1 and i < size-1:
            if board[i+1][j+1] == 'b':
                result.append(move_right_down(board,[i,j]))
        if i < size-1:
            if board[i+1][j] == '-':
                result.append(move_down(board,[i,j]))
    return result

def blackMoves(board,size):
    result = []
    num_black = 0
    index_black = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == "b":
                num_black += 1
                index_black.append([i,j])
    for k in index_black:
        i = k[0]
        j = k[1]
        if j >= 1 and i > 0:
            if board[i-1][j-1] == 'w':
                result.append(move_left_up(board,[i,j]))
        if j < size-1 and i > 0:
            if board[i-1][j+1] == 'w':
                result.append(move_right_up(board,[i,j]))
        if i > 0:
            if board[i-1][j] == '-':
                result.append(move_up(board,[i,j]))
    return result

## These are helper functions for the pawns so they could move in a certain direction
## They all return one state 
def move_up(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i-1][j] = 'b'
    return state

def move_down(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i+1][j] = 'w'
    return state

def move_left_down(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i+1][j-1] = 'w'
    return state

def move_right_down(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i+1][j+1] = 'w'
    return state

def move_left_up(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i-1][j-1] = 'b'
    return state

def move_right_up(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i-1][j+1] = 'b'
    return state

## This function is a helpful that convert the input list of string to a list of lists
## This function takes one parameter: the state
def hexagame(start):
    arr = []
    for i in range(len(start)):
        arr.append(list(start[i]))
    return arr

## This function is a helpful for minimax search to sort the values from lowest to highest
#list of valuess is the only parameter
def insertionSort(values):
    i = 1
    while i < len(values):
        key = values[i]
        j = i-1
        while j>=0 and values[j]>key:
            values[j+1] = values[j]
            j -= 1
        values[j+1] = key
        i += 1
    return 

## This function is a helpful for minimax search to sort the values from lowest to highest and their correspond states
def insertionSortB(values,states):
    i = 1
    while i < len(values):
        key = values[i]
        key2 = states[i]
        j = i-1
        while j>=0 and values[j]>key:
            values[j+1] = values[j]
            states[j+1] = states[j]
            j -= 1
        values[j+1] = key
        states[j+1] = key2
        i += 1
    return
