import pygame
import sys
import os
import random
from datetime import datetime

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
PLAYER1_COLOR = (219, 68, 55)  # Red for Player 1
PLAYER2_COLOR = (66, 134, 244)  # Blue for Player 2
DRAW_COLOR = WHITE  # Plain white for draws
BUTTON_COLOR = (173, 216, 230)
BUTTON_HOVER_COLOR = (135, 206, 250)
BUTTON_PRESSED_COLOR = (100, 149, 237)

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
player1_wins = 0
player2_wins = 0
draws = 0

class Button:
    def __init__(self, x, y, width, height, text, action, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.default_color = color
        self.hovered = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, border_radius=10)
        text_surface = TITLE_FONT.render(self.text, True, BLACK)
        win.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.action == "quit":
            pygame.quit()
            sys.exit()
        else:
            self.color = BUTTON_PRESSED_COLOR
            pygame.display.update()
            pygame.time.delay(300)
            os.system(f'python {self.action}')

    def on_hover(self):
        if not self.hovered:
            self.color = BUTTON_HOVER_COLOR
            self.hovered = True

    def reset_color(self):
        if self.hovered:
            self.color = self.default_color
            self.hovered = False

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
    global player1_wins, player2_wins, draws
    if winner == 'X':
        player1_wins += 1
    elif winner == 'O':
        player2_wins += 1
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
    pygame.draw.rect(WINDOW, PLAYER1_COLOR, (0, HEIGHT - SCOREBOARD_HEIGHT, WIDTH // 3, SCOREBOARD_HEIGHT))
    pygame.draw.rect(WINDOW, DRAW_COLOR, (WIDTH // 3, HEIGHT - SCOREBOARD_HEIGHT, WIDTH // 3, SCOREBOARD_HEIGHT))
    pygame.draw.rect(WINDOW, PLAYER2_COLOR, (2 * WIDTH // 3, HEIGHT - SCOREBOARD_HEIGHT, WIDTH // 3, SCOREBOARD_HEIGHT))

    player1_text = f"PLAYER 1"
    player2_text = f"PLAYER 2"
    draw_text = f"DRAW"

    player1_score = f"{player1_wins}"
    player2_score = f"{player2_wins}"
    draw_score = f"{draws}"

    player1_surface = TITLE_FONT.render(player1_text, True, BLACK)
    player2_surface = TITLE_FONT.render(player2_text, True, BLACK)
    draw_surface = TITLE_FONT.render(draw_text, True, BLACK)

    player1_score_surface = TITLE_FONT.render(player1_score, True, BLACK)
    player2_score_surface = TITLE_FONT.render(player2_score, True, BLACK)
    draw_score_surface = TITLE_FONT.render(draw_score, True, BLACK)

    # Draw text centered in their respective areas
    WINDOW.blit(player1_surface, ((WIDTH // 3 - player1_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 10))
    WINDOW.blit(draw_surface, (WIDTH // 3 + (WIDTH // 3 - draw_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 10))
    WINDOW.blit(player2_surface, (2 * WIDTH // 3 + (WIDTH // 3 - player2_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 10))

    WINDOW.blit(player1_score_surface, ((WIDTH // 3 - player1_score_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 70))
    WINDOW.blit(draw_score_surface, (WIDTH // 3 + (WIDTH // 3 - draw_score_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 70))
    WINDOW.blit(player2_score_surface, (2 * WIDTH // 3 + (WIDTH // 3 - player2_score_surface.get_width()) // 2, HEIGHT - SCOREBOARD_HEIGHT + 70))

def draw_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    time_surface = TITLE_FONT.render(current_time, True, BLACK)
    WINDOW.blit(time_surface, (WIDTH - time_surface.get_width() - 20, 20))

def main():
    global current_player, game_over, winner

    # Create 'X' quit button
    quit_button = Button(10, 10, 50, 50, "X", "quit")

    # Main game loop
    while True:
        WINDOW.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if quit_button.is_hovered(pos):
                    quit_button.click()

                if not game_over:
                    for row in range(BOARD_ROWS):
                        for col in range(BOARD_COLS):
                            if board[row][col] == '' and GRID_TOP_LEFT_X + col * SQUARE_SIZE < pos[0] < GRID_TOP_LEFT_X + (col + 1) * SQUARE_SIZE and GRID_TOP_LEFT_Y + row * SQUARE_SIZE < pos[1] < GRID_TOP_LEFT_Y + (row + 1) * SQUARE_SIZE:
                                board[row][col] = current_player
                                if check_win(board, current_player):
                                    winner = current_player
                                    game_over = True
                                    draw_winner(winner)
                                elif is_draw(board):
                                    winner = None
                                    game_over = True
                                    draw_winner(winner)
                                else:
                                    current_player = 'O' if current_player == 'X' else 'X'

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if quit_button.is_hovered(pos):
                    quit_button.on_hover()
                else:
                    quit_button.reset_color()

        draw_grid()
        draw_board()
        update_scoreboard()
        draw_clock()
        quit_button.draw(WINDOW)
        pygame.display.update()

if __name__ == "__main__":
    main()
