import pygame
import sys
import random
from datetime import datetime
from time import sleep

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
SCOREBOARD_HEIGHT = 150  # Define the height of the scoreboard
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // 8  # Make the square size smaller
GRID_WIDTH = SQUARE_SIZE * BOARD_COLS
GRID_HEIGHT = SQUARE_SIZE * BOARD_ROWS
GRID_TOP_LEFT_X = (WIDTH - GRID_WIDTH) // 2
GRID_TOP_LEFT_Y = (HEIGHT - SCOREBOARD_HEIGHT - GRID_HEIGHT) // 2

# Colors
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = BLACK
BG_COLOR = WHITE
X_COLOR = (66, 134, 244)
O_COLOR = (219, 68, 55)
PLAYER_COLOR = (219, 68, 55)  # Red for Player
AI_COLOR = (66, 134, 244)  # Blue for AI
DRAW_COLOR = WHITE  # Plain white for draws

# Fonts
TITLE_FONT = pygame.font.SysFont('comicsans', 60)
END_FONT = pygame.font.SysFont('comicsans', 40)
LETTER_FONT = pygame.font.SysFont('comicsans', 80)

# Initialize game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Tic Tac Toe")

# Initialize game variables
current_player = 'X'
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
game_over = False
winner = None
player_wins = 0
ai_wins = 0
draws = 0

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = BLACK
        self.hover_color = X_COLOR
        self.current_color = self.color

    def draw(self, win):
        pygame.draw.rect(win, self.current_color, self.rect)
        font = pygame.font.SysFont('comicsans', 40)
        text_surf = font.render(self.text, True, WHITE)
        win.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def on_hover(self):
        self.current_color = self.hover_color

    def reset_color(self):
        self.current_color = self.color

    def click(self):
        if self.action:
            if self.action == "quit":
                pygame.quit()
                sys.exit()

def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(WINDOW, LINE_COLOR, (GRID_TOP_LEFT_X, GRID_TOP_LEFT_Y + i * SQUARE_SIZE), 
                         (GRID_TOP_LEFT_X + GRID_WIDTH, GRID_TOP_LEFT_Y + i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(WINDOW, LINE_COLOR, (GRID_TOP_LEFT_X + i * SQUARE_SIZE, GRID_TOP_LEFT_Y), 
                         (GRID_TOP_LEFT_X + i * SQUARE_SIZE, GRID_TOP_LEFT_Y + GRID_HEIGHT), LINE_WIDTH)

def draw_board():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                text_surface = LETTER_FONT.render('X', True, X_COLOR)
                WINDOW.blit(text_surface, (GRID_TOP_LEFT_X + col * SQUARE_SIZE + (SQUARE_SIZE - text_surface.get_width()) // 2, GRID_TOP_LEFT_Y + row * SQUARE_SIZE + (SQUARE_SIZE - text_surface.get_height()) // 2))
            elif board[row][col] == 'O':
                text_surface = LETTER_FONT.render('O', True, O_COLOR)
                WINDOW.blit(text_surface, (GRID_TOP_LEFT_X + col * SQUARE_SIZE + (SQUARE_SIZE - text_surface.get_width()) // 2, GRID_TOP_LEFT_Y + row * SQUARE_SIZE + (SQUARE_SIZE - text_surface.get_height()) // 2))

def draw_winner(winner):
    global player_wins, ai_wins, draws
    if winner == 'X':
        player_wins += 1
    elif winner == 'O':
        ai_wins += 1
    else:
        draws += 1

    update_scoreboard()

    if winner:
        win_text = f"Player {winner} wins!"
    else:
        win_text = "It's a draw!"

    text_surface = END_FONT.render(win_text, True, BLACK)
    pygame.draw.rect(WINDOW, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 150))
    pygame.draw.rect(WINDOW, BLACK, (WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 150), 5)
    WINDOW.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

    reset_game()

def check_win(board, player):
    # Check rows
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_draw(board):
    for row in board:
        for val in row:
            if val == '':
                return False
    return True

def reset_game():
    global board, current_player, game_over, winner
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    current_player = 'X'
    game_over = False
    winner = None

def update_scoreboard():
    pygame.draw.rect(WINDOW, PLAYER_COLOR, (0, HEIGHT - SCOREBOARD_HEIGHT, WIDTH // 3, SCOREBOARD_HEIGHT))
    pygame.draw.rect(WINDOW, DRAW_COLOR, (WIDTH // 3, HEIGHT - SCOREBOARD_HEIGHT, WIDTH // 3, SCOREBOARD_HEIGHT))
    pygame.draw.rect(WINDOW, AI_COLOR, (2 * WIDTH // 3, HEIGHT - SCOREBOARD_HEIGHT, WIDTH // 3, SCOREBOARD_HEIGHT))

    player_text = f"PLAYER"
    ai_text = f"AI"
    draw_text = f"DRAW"

    player_score = f"{player_wins}"
    ai_score = f"{ai_wins}"
    draw_score = f"{draws}"

    player_surface = TITLE_FONT.render(player_text, True, BLACK)
    ai_surface = TITLE_FONT.render(ai_text, True, BLACK)
    draw_surface = TITLE_FONT.render(draw_text, True, BLACK)

    player_score_surface = TITLE_FONT.render(player_score, True, BLACK)
    ai_score_surface = TITLE_FONT.render(ai_score, True, BLACK)
    draw_score_surface = TITLE_FONT.render(draw_score, True, BLACK)

    # Draw text centered in their respective areas
    WINDOW.blit(player_surface, ((WIDTH // 3 - player_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 10))
    WINDOW.blit(draw_surface, (WIDTH // 3 + (WIDTH // 3 - draw_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 10))
    WINDOW.blit(ai_surface, (2 * WIDTH // 3 + (WIDTH // 3 - ai_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 10))

    WINDOW.blit(player_score_surface, ((WIDTH // 3 - player_score_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 70))
    WINDOW.blit(draw_score_surface, (WIDTH // 3 + (WIDTH // 3 - draw_score_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 70))
    WINDOW.blit(ai_score_surface, (2 * WIDTH // 3 + (WIDTH // 3 - ai_score_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 70))

def draw_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    time_surface = TITLE_FONT.render(current_time, True, BLACK)
    WINDOW.blit(time_surface, (WIDTH - time_surface.get_width() - 20, 20))

def ai_move():
    sleep(1)  # Simulate AI thinking time
    empty_squares = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == '']
    
    # Basic AI strategy: first try to win, then block, then random
    for (row, col) in empty_squares:
        board[row][col] = 'O'
        if check_win(board, 'O'):
            return
        board[row][col] = ''
    
    for (row, col) in empty_squares:
        board[row][col] = 'X'
        if check_win(board, 'X'):
            board[row][col] = 'O'
            return
        board[row][col] = ''
    
    row, col = random.choice(empty_squares)
    board[row][col] = 'O'

# Create quit button
quit_button = Button(10, 10, 50, 50, "X", action="quit")

def main():
    global current_player, game_over, winner

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_hovered(pos):
                    quit_button.click()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 'X':
                mouseX = (event.pos[0] - GRID_TOP_LEFT_X) // SQUARE_SIZE
                mouseY = (event.pos[1] - GRID_TOP_LEFT_Y) // SQUARE_SIZE

                if 0 <= mouseX < BOARD_COLS and 0 <= mouseY < BOARD_ROWS:
                    if board[mouseY][mouseX] == '':
                        board[mouseY][mouseX] = current_player
                        if check_win(board, current_player):
                            winner = current_player
                            game_over = True
                        elif is_draw(board):
                            game_over = True
                        current_player = 'O'

                        # Update display after player move
                        WINDOW.fill(BG_COLOR)
                        draw_grid()
                        draw_board()
                        update_scoreboard()
                        draw_clock()
                        quit_button.draw(WINDOW)
                        pygame.display.update()

        if current_player == 'O' and not game_over:
            ai_move()
            if check_win(board, 'O'):
                winner = 'O'
                game_over = True
            elif is_draw(board):
                game_over = True
            current_player = 'X'

        if game_over:
            draw_winner(winner if winner else 'Draw')

        # Update hover effect
        if quit_button.is_hovered(pos):
            quit_button.on_hover()
        else:
            quit_button.reset_color()

        # Regularly update display
        WINDOW.fill(BG_COLOR)
        draw_grid()
        draw_board()
        update_scoreboard()
        draw_clock()
        quit_button.draw(WINDOW)
        pygame.display.update()

main()
