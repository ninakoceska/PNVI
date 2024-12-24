import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

# Size of the grid (5x5)
GRID_SIZE = 5
# Size of each cell in the grid
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Define colors in RGB format
COLORS = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0)
}

# List of color keys (without white, since that's used as the background)
COLOR_KEYS = list(COLORS.keys())[1:]

# Initialize the screen and set its caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

# Initialize the 5x5 grid, each cell starts as None (uncolored)
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to draw the grid and fill cells with colors
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # If the cell has a color, use that color, otherwise, use white
            color = COLORS[grid[row][col]] if grid[row][col] else COLORS["white"]
            # Draw the rectangle (square) for each grid cell
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Draw a black border around each cell
            pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to get the grid cell (row, col) based on mouse position
def get_cell(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

# Function to check if the color is valid for the selected cell
def is_valid_color(row, col, color):
    # Check the neighboring cells (top, bottom, left, right)
    neighbors = [
        (row - 1, col), (row + 1, col),  # Top, Bottom
        (row, col - 1), (row, col + 1)   # Left, Right
    ]
    # If any of the neighbors has the same color, it's not a valid color
    for r, c in neighbors:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and grid[r][c] == color:
            return False
    return True

# Function to check if the player has won (all squares filled with valid colors)
def check_win():
    # Go through all the grid cells and check if they are filled with valid colors
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # If a cell is empty or its color is invalid, the player hasn't won yet
            if not grid[row][col] or not is_valid_color(row, col, grid[row][col]):
                return False
    return True

# Start the game loop
selected_color = COLOR_KEYS[0]  # Default color is red (first color in COLOR_KEYS)
running = True

# Main game loop
while running:
    screen.fill(COLORS["white"])  # Fill the background with white
    draw_grid()  # Draw the grid with current colors

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game if the window is closed
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # When the mouse is clicked, get the cell position and color it
            row, col = get_cell(pygame.mouse.get_pos())
            # Only color the cell if the selected color is valid for that cell
            if is_valid_color(row, col, selected_color):
                grid[row][col] = selected_color
        elif event.type == pygame.KEYDOWN:
            # Change the selected color based on the key pressed
            if event.key == pygame.K_1:
                selected_color = "red"
            elif event.key == pygame.K_2:
                selected_color = "green"
            elif event.key == pygame.K_3:
                selected_color = "blue"
            elif event.key == pygame.K_4:
                selected_color = "yellow"

    # Check if the player has won and display a message
    if check_win():
        font = pygame.font.Font(None, 50)  # Create font object
        text = font.render("You Win!", True, (0, 0, 0))  # Create text surface
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
