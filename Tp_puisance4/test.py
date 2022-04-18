import random
import sys
import math
from tkinter import *
import numpy as np
import pygame
from pygame import mixer

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
beige = (222, 184, 135)

PLAYER = 0
AI = 1

EMPTY = 0

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

GAGNANT_AI = 3
GAGNANT_PLAYER = 4

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100

RADIUS = int(SQUARESIZE / 2 - 5)


def create_board():  # lespace du jeux
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):  # la piece du jeux
    board[row][col] = piece

def is_valid_location(board, col):  # si la case est vide ou pa
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))  # n3aksso matrice

def coup_gangne(board, piece):
    # gange horizental
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    # gange vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True
    # diagonal +
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True
    # diagonal -
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    if piece==AI_PIECE:
        if window.count(piece) == 4:
            score += 100
        if window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        if window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
    if piece==PLAYER_PIECE:
        if window.count(piece) == 3 and window.count(EMPTY) == 1:
            score -= 5
        if window.count(piece) == 2 and window.count(EMPTY) == 2:
            score -= 2
    return score


def Evaluation(board, piece):
    score = 0
    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def score(board, piece):
    # nssarbiw la fonction 'evaluate' bache n7assbo le score ta3 la matrice binissba lal player dyana: player0
    eval_0 = Evaluation(board, 1)
    # nssarbiw la fonction 'evaluate' bache n7assbo le score ta3 la matrice binissba lal player dyana: player1
    eval_1 = Evaluation(board, 2)
    # tmatal chkon rah yal3ab (fal 7ala dyana aw dal IA kayal3ab).
    if piece == PLAYER_PIECE:
        return eval_0 - eval_1
    else:
        return eval_1 - eval_0


def list_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_terminal_node(board):
    # si l'utilisateur gangné ou bien la machine sinn tous les cases sont complet
    return coup_gangne(board, PLAYER_PIECE) or coup_gangne(board, AI_PIECE) or len(list_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = list_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if coup_gangne(board, AI_PIECE):
                return (None, 100000000000000)
            elif coup_gangne(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:  # Depth is zero
            return (None, score(board, AI_PIECE))
        # return (None, Evaluation(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Min player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


# -------------------------------------------dessin interface du jeux (board of game)---------------------------------------------------------
def draw_board(board,image_player):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, beige, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            screen.blit(pygame.transform.scale(image_player, (SQUARESIZE,SQUARESIZE)),
                        (c * SQUARESIZE-2, r * SQUARESIZE + SQUARESIZE-2))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == GAGNANT_AI:
                pygame.draw.circle(screen, GREEN, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS - 15)
            elif board[r][c] == GAGNANT_PLAYER:
                pygame.draw.circle(screen, GREEN, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS - 15)

    pygame.display.update()


# -----------------------------------------------------------------------
board = create_board()
print_board(board)

root = Tk()
frame = Frame(root)

frame.pack()
root.geometry('350x350')
root.config(bg='Black')
root.title("Puissance 4")

img = PhotoImage(file="fenetre.png")  # background la premier fentre
p1 = PhotoImage(file='connect.png')  # icon de fentre


def play():
    pygame.init()
    root.destroy()


# Setting icon of master window
root.iconphoto(False, p1)
label = Label(root, image=img)
label.place(x=0, y=0)
button = Button(root, text='Play', fg='white', font=('calibri', 15), width=8, command=play, activebackground='blue',bg='blue')
button.place(x=180, y=280)
button = Button(root, text='Quit', fg='white', font=('calibri', 15), width=8, command=exit, activebackground='blue',bg='red')
button.place(x=50, y=280)
root.mainloop()
pygame.display.set_caption('Puissance 4')
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
image_player=pygame.image.load('téléchargement__5_-removebg-preview.png').convert()
draw_board(board,image_player)
turn = random.randint(PLAYER, AI)
img = pygame.image.load('connect.jpg').convert()
pygame.display.set_icon(img)
back_g = pygame.image.load("Game Over !!!! (1).png").convert()
back_win = pygame.image.load("win.png").convert()


pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
game_over = False
AI_gagne = False
player_gagne = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            button_press_time = pygame.time.get_ticks()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            # Player 1 -----utilisateur
            if turn == PLAYER:
                p_s = mixer.Sound("bang.wav")
                p_s.play()
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if coup_gangne(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                        player_gagne = True
                        p_s = mixer.Sound("winner.wav")
                        p_s.play()
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board,image_player)
                # Player 2 -----machine
    if turn == AI and not game_over:
        p_s1 = mixer.Sound("bang.wav")
        p_s1.play()
        # col= random.randint(0, COLUMN_COUNT-1)
        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if coup_gangne(board, AI_PIECE):
                label = myfont.render("Machine Gangné!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
                AI_gagne = True
                p_s = mixer.Sound("lost.wav")
                p_s.play()
            draw_board(board,image_player)
            turn += 1
            turn = turn % 2
    if game_over and AI_gagne:
        pygame.time.wait(3000)
        screen.blit(back_g, [0, 0])
        pygame.display.update()
        pygame.time.wait(4000)

    # pygame.time.wait(3000)
    elif game_over and player_gagne:
        pygame.time.wait(3000)
        screen.blit(back_win, [0, 0])
        pygame.display.update()
        pygame.time.wait(4000)
    elif game_over and not AI_PIECE and not player_gagne:
        print("joue terminé invalid location")
        pygame.quit()
        sys.exit()

# pygame.quit()
# sys.exit()
