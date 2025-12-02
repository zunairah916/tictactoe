import pygame as pygame
import sys

WIDTH, HEIGHT = 480, 600        
CELL = WIDTH // 3
LINE_WIDTH = 6
CROSS_WIDTH = 12
CIRCLE_WIDTH = 8
PADDING = 20
FPS = 60

BG = (28, 28, 28)
LINE_COLOR = (240, 240, 240)
X_COLOR = (220, 80, 80)
O_COLOR = (80, 160, 220)
HIGHLIGHT_COLOR = (100, 255, 100)
RESULT_COLOR = (120, 220, 200)


def empty_board():
    return (' ',) * 9

WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,6),(1,4,7),(2,5,8),
             (0,4,8),(2,4,6)]

def print_board(board):
    for i in range(3):
        print(board[i*3:(i+1)*3])
    print()

def is_terminal(board):
    for a,b,c in WIN_LINES:
        if board[a] == board[b] == board[c] != ' ':
            return True, board[a]
    if ' ' not in board:
        return True, 'Draw'
    return False, None

def rotations_and_reflections(board):
    b = board
    def rot90(b):
        return (b[6], b[3], b[0],
                b[7], b[4], b[1],
                b[8], b[5], b[2])
    def reflect(b):
        return (b[2], b[1], b[0],
                b[5], b[4], b[3],
                b[8], b[7], b[6])
    variants = []
    cur = b
    for _ in range(4):
        variants.append(cur)
        variants.append(reflect(cur))
        cur = rot90(cur)
    return variants

def canonical(board, player):
    variants = rotations_and_reflections(board)
    return (min(variants), player)


memo = {}

def minimax(board, player, alpha=-2, beta=2):
    key = canonical(board, player)
    if key in memo:
        return memo[key]

    terminal, winner = is_terminal(board)
    if terminal:
        if winner == 'Draw':
            return 0
        return 1 if winner == 'X' else -1

    if player == 'X':
        value = -2
        for i in range(9):
            if board[i] == ' ':
                nb = board[:i] + ('X',) + board[i+1:]
                score = minimax(nb, 'O', alpha, beta)
                if score > value:
                    value = score
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
    else:
        value = 2
        for i in range(9):
            if board[i] == ' ':
                nb = board[:i] + ('O',) + board[i+1:]
                score = minimax(nb, 'X', alpha, beta)
                if score < value:
                    value = score
                beta = min(beta, value)
                if beta <= alpha:
                    break

    memo[key] = value
    return value

def best_move(board, player):
    best_moves = []
    if player == 'X':
        best_val = -2
        for i in range(9):
            if board[i] == ' ':
                nb = board[:i] + ('X',) + board[i+1:]
                val = minimax(nb, 'O')
                if val > best_val:
                    best_val = val
                    best_moves = [i]
                elif val == best_val:
                    best_moves.append(i)
    else:
        best_val = 2
        for i in range(9):
            if board[i] == ' ':
                nb = board[:i] + ('O',) + board[i+1:]
                val = minimax(nb, 'X')
                if val < best_val:
                    best_val = val
                    best_moves = [i]
                elif val == best_val:
                    best_moves.append(i)

    order = [4,0,2,6,8,1,3,5,7]
    for o in order:
        if o in best_moves:
            return o
    return best_moves[0] if best_moves else None
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)

def draw_grid():
    pygame.draw.line(screen, LINE_COLOR, (CELL, 0), (CELL, CELL*3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (CELL*2, 0), (CELL*2, CELL*3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL), (CELL*3, CELL), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL*2), (CELL*3, CELL*2), LINE_WIDTH)

def cell_center(index):
    r = index // 3
    c = index % 3
    return c*CELL + CELL//2, r*CELL + CELL//2

def draw_X(index):
    x, y = cell_center(index)
    o = CELL//2 - PADDING
    pygame.draw.line(screen, X_COLOR, (x-o, y-o), (x+o, y+o), CROSS_WIDTH)
    pygame.draw.line(screen, X_COLOR, (x-o, y+o), (x+o, y-o), CROSS_WIDTH)

def draw_O(index):
    x, y = cell_center(index)
    radius = CELL//2 - PADDING
    pygame.draw.circle(screen, O_COLOR, (x, y), radius, CIRCLE_WIDTH)

def highlight_line(line):
    a, b, c = line
    pygame.draw.line(screen, HIGHLIGHT_COLOR, cell_center(a), cell_center(c), 8)

board = empty_board()
current_player = 'X'
game_over = False
winner_line = None
show_help = True

def index_from_pos(pos):
    x, y = pos
    if y >= CELL*3:
        return None
    return (y // CELL) * 3 + (x // CELL)

def find_winning_line(board):
    for a,b,c in WIN_LINES:
        if board[a] == board[b] == board[c] != ' ':
            return (a,b,c)
    return None

def reset(new_first='X'):
    global board, current_player, game_over, winner_line, show_help
    board = empty_board()
    current_player = new_first
    game_over = False
    winner_line = None
    show_help = False

BTN_RESTART = pygame.Rect(10, CELL*3 + 10, 130, 40)
BTN_FIRST = pygame.Rect(170, CELL*3 + 10, 150, 40)


if current_player == 'X':
    ai_move = best_move(board, 'X')
    if ai_move is not None:
        board = board[:ai_move] + ('X',) + board[ai_move+1:]
        current_player = 'O'

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if BTN_RESTART.collidepoint((mx,my)):
                reset(current_player)
                if current_player == 'X':
                    ai = best_move(board,'X')
                    if ai is not None:
                        board = board[:ai] + ('X',) + board[ai+1:]
                        current_player='O'
                continue

            if BTN_FIRST.collidepoint((mx,my)):
                current_player = 'O' if current_player == 'X' else 'X'
                reset(current_player)
                if current_player == 'X':
                    ai = best_move(board,'X')
                    if ai is not None:
                        board = board[:ai] + ('X',) + board[ai+1:]
                        current_player='O'
                continue

            if not game_over:
                idx = index_from_pos((mx,my))
                if idx is not None and board[idx]==' ' and current_player=='O':
                    board = board[:idx] + ('O',) + board[idx+1:]
                    t, w = is_terminal(board)
                    if t:
                        game_over = True
                        if w != 'Draw':
                            winner_line = find_winning_line(board)
                        current_player = 'X'
                    else:
                        current_player = 'X'
                        ai = best_move(board,'X')
                        if ai is not None:
                            board = board[:ai] + ('X',) + board[ai+1:]
                        t, w = is_terminal(board)
                        if t:
                            game_over=True
                            if w != 'Draw':
                                winner_line = find_winning_line(board)
                        current_player = 'O'

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset(current_player)

    screen.fill(BG)
    draw_grid()

    for i,c in enumerate(board):
        if c == 'X': draw_X(i)
        elif c == 'O': draw_O(i)

    if winner_line:
        highlight_line(winner_line)

    pygame.draw.rect(screen, (20,20,20), (0, CELL*3, WIDTH, HEIGHT - CELL*3))
    pygame.draw.rect(screen, (70,70,70), BTN_RESTART)
    pygame.draw.rect(screen, (70,70,70), BTN_FIRST)

    screen.blit(font.render("Restart (R)", True, LINE_COLOR), (20, CELL*3 + 18))
    screen.blit(font.render("Toggle Start", True, LINE_COLOR), (180, CELL*3 + 18))

    if show_help:
        help_lines = [
            "Click a cell to play as O.",
            "AI uses perfect Minimax.",
            "Toggle who starts anytime."
        ]
        for i, ln in enumerate(help_lines):
            screen.blit(font.render(ln, True, LINE_COLOR),
                        (10, CELL*3 - 100 + i*22))

    if game_over:
        t, w = is_terminal(board)
        msg = "It's a draw!" if w=="Draw" else f"{w} wins!"
        screen.blit(big_font.render(msg, True, RESULT_COLOR),
                    (18, CELL*3 + 60))

    pygame.display.flip()

pygame.quit()
sys.exit()
