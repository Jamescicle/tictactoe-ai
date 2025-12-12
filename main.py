import msvcrt
import random

# chance (0-1) to make a random move instead of optimal
AIRANDOMCHANCE = 0.1 

def createBoard():
    return [["#" for _ in range(3)] for _ in range(3)]

def prettyPrintBoard(board, cursorx=None, cursory=None):
    for y in range(3):
        row_display = []
        for x in range(3):
            cell = board[x][y]
            # player curosr
            if cursorx == x and cursory == y:
                row_display.append(f"[{cell}]")
            else:
                row_display.append(f" {cell} ")
        print(" ".join(row_display))

def getInput():
    if msvcrt.kbhit():
        key = msvcrt.getch().lower()
        if key == b'w':  # up
            return 'up'
        elif key == b's':  # down
            return 'down'
        elif key == b'a':  # left
            return 'left'
        elif key == b'd':  # right
            return 'right'
        elif key == b'\r':  # enter
            return 'select'
    return None

def checkWinner(board):
    for row in range(3):
        if board[0][row] == board[1][row] == board[2][row] != '#':
            return board[0][row]
    
    for col in range(3):
        if board[col][0] == board[col][1] == board[col][2] != '#':
            return board[col][0]
    
    if board[0][0] == board[1][1] == board[2][2] != '#':
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] != '#':
        return board[2][0]
    
    return None

def isBoardFull(board):
    for row in board:
        if '#' in row:
            return False
    return True

def minimaxthingy(board, depth, is_maximizing):
    winner = checkWinner(board)
    
    if winner == 'O':
        return 10 - depth
    elif winner == 'X':
        return depth - 10
    elif isBoardFull(board):
        return 0  # draw
    
    if is_maximizing:
        # computers turn maximize score
        best_score = -float('inf')
        for x in range(3):
            for y in range(3):
                if board[x][y] == '#':
                    board[x][y] = 'O'
                    score = minimaxthingy(board, depth + 1, False)
                    board[x][y] = '#'
                    best_score = max(score, best_score)
        return best_score
    else:
        # players turn minimize score
        best_score = float('inf')
        for x in range(3):
            for y in range(3):
                if board[x][y] == '#':
                    board[x][y] = 'X'
                    score = minimaxthingy(board, depth + 1, True)
                    board[x][y] = '#'
                    best_score = min(score, best_score)
        return best_score

def getBestMove(board):
    # chance to do random move
    if random.random() < AIRANDOMCHANCE:
        empty_moves = [(x, y) for x in range(3) for y in range(3) if board[x][y] == '#']
        if empty_moves:
            return random.choice(empty_moves)
    
    best_score = -float('inf')
    best_move = None
    
    for x in range(3):
        for y in range(3):
            if board[x][y] == '#':
                board[x][y] = 'O'
                score = minimaxthingy(board, 0, False)
                board[x][y] = '#'
                
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
    
    return best_move

def play_game():
    board = createBoard()
    cursorx, cursory = 0, 0
    
    # print board
    print("\033[2J")  # clear screen (i did not know this until 5m ago lmao)
    print("Use WASD to move, Enter to place X")
    prettyPrintBoard(board, cursorx, cursory)
    
    while True:
        action = getInput()
        
        if action == 'up':
            cursory = max(0, cursory - 1)
        elif action == 'down':
            cursory = min(2, cursory + 1)
        elif action == 'left':
            cursorx = max(0, cursorx - 1)
        elif action == 'right':
            cursorx = min(2, cursorx + 1)
        elif action == 'select':
            if board[cursorx][cursory] == '#':
                board[cursorx][cursory] = 'X'
                if checkWinner(board) == 'X':
                    print("\033[2J")
                    prettyPrintBoard(board)
                    print("You win!")
                    break
                if isBoardFull(board):
                    print("\033[2J")
                    prettyPrintBoard(board)
                    print("It's a draw!")
                    break
                
                # ai turn
                print("\033[2J")
                print("Thinking...")
                ai_move = getBestMove(board)
                if ai_move:
                    board[ai_move[0]][ai_move[1]] = 'O'
                    
                    if checkWinner(board) == 'O':
                        print("\033[2J")
                        prettyPrintBoard(board)
                        print("AI wins!")
                        break
                    
                    if isBoardFull(board):
                        print("\033[2J")
                        prettyPrintBoard(board)
                        print("It's a draw!")
                        break
                
                print("\033[2J")
                prettyPrintBoard(board, cursorx, cursory)
                continue
        
        if action:
            print("\033[2J")
            prettyPrintBoard(board, cursorx, cursory)

play_game()

