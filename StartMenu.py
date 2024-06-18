import pygame
import sys
import os
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_SPACING = 40
FONT_SIZE = 60
SMALL_FONT_SIZE = 40

# Colors
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_COLOR = (66, 134, 244)
O_COLOR = (219, 68, 55)
BUTTON_COLOR = (173, 216, 230)
BUTTON_HOVER_COLOR = (135, 206, 250)
BUTTON_PRESSED_COLOR = (100, 149, 237)
TEXT_COLOR = BLACK

# Fonts
TITLE_FONT = pygame.font.SysFont('comicsans', FONT_SIZE)
BUTTON_FONT = pygame.font.SysFont('comicsans', SMALL_FONT_SIZE)
MADE_BY_FONT = pygame.font.SysFont('comicsans', SMALL_FONT_SIZE // 2)

# Initialize game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Tic Tac Toe")

# Load background music
pygame.mixer.music.load('background_music.mp3')  # Ensure the correct path to your music file
pygame.mixer.music.play(-1)  # Play the music in a loop

# Load textures
class BackgroundElement:
    def __init__(self, text, x, y, speed):
        self.text = text
        self.x = x
        self.y = y
        self.speed = speed
        self.surface = TITLE_FONT.render(text, True, X_COLOR if text == 'X' else O_COLOR)

    def draw(self, win):
        win.blit(self.surface, (self.x, self.y))
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.surface.get_height()
            self.x = random.randint(0, WIDTH)

background_elements = [
    BackgroundElement('X', random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.3, 0.5))
    for _ in range(5)
] + [
    BackgroundElement('O', random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.3, 0.5))
    for _ in range(5)
]

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.hovered = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, border_radius=10)
        text_surface = BUTTON_FONT.render(self.text, True, TEXT_COLOR)
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

# Main menu function
def main_menu():
    run = True
    clock = pygame.time.Clock()

    buttons = [
        Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 2 * BUTTON_HEIGHT - 1 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "2 PLAYERS", "PvP.py"),
        Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, "AI - EASY", "Easy.py"),
        Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT + 1 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "AI - HARD", "Hard.py"),
    ]

    x_label = Button(10, 10, 50, 50, "X", "quit", color=GRAY)  # Use GRAY color for the X button

    while run:
        WINDOW.fill(WHITE)

        for element in background_elements:
            element.draw(WINDOW)

        title_surface = TITLE_FONT.render("Tic Tac Toe", True, BLACK)
        WINDOW.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

        for button in buttons:
            button.draw(WINDOW)

        x_label.draw(WINDOW)

        made_by_surface = MADE_BY_FONT.render("Made by Travis", True, BLACK)
        WINDOW.blit(made_by_surface, (WIDTH // 2 - made_by_surface.get_width() // 2, HEIGHT - 50))

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons + [x_label]:
                    if button.is_hovered(pos):
                        button.click()

        # Update button colors based on hover state
        for button in buttons + [x_label]:
            if button.is_hovered(pygame.mouse.get_pos()):
                button.color = BUTTON_HOVER_COLOR
            else:
                button.color = BUTTON_COLOR  # Reset to default color when not hovered

        pygame.display.update()
        clock.tick(60)  # Higher frame rate for smoother transitions

    pygame.quit()
    sys.exit()

main_menu()