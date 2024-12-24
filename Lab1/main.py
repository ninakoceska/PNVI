import pygame
import sys


pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
GRID_SIZE = 5
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
COLORS = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0)
}
COLOR_KEYS = list(COLORS.keys())[1:]


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")


grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]



def draw_grid():

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = COLORS[grid[row][col]] if grid[row][col] else COLORS["white"]
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def get_cell(pos):

    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE


def is_valid_color(row, col, color):

    neighbors = [
        (row - 1, col), (row + 1, col),  # Top, Bottom
        (row, col - 1), (row, col + 1)  # Left, Right
    ]
    for r, c in neighbors:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and grid[r][c] == color:
            return False
    return True


def check_win():

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if not grid[row][col] or not is_valid_color(row, col, grid[row][col]):
                return False
    return True



selected_color = COLOR_KEYS[0]
running = True
while running:
    screen.fill(COLORS["white"])
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_cell(pygame.mouse.get_pos())
            if is_valid_color(row, col, selected_color):
                grid[row][col] = selected_color
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_color = "red"
            elif event.key == pygame.K_2:
                selected_color = "green"
            elif event.key == pygame.K_3:
                selected_color = "blue"
            elif event.key == pygame.K_4:
                selected_color = "yellow"

    if check_win():
        font = pygame.font.Font(None, 50)
        text = font.render("You Win!", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
