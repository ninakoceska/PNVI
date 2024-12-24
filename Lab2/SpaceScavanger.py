import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800  # Screen width in pixels
SCREEN_HEIGHT = 600  # Screen height in pixels
FPS = 60  # Frames per second

# Colors
WHITE = (255, 255, 255)  # White color for background

# Load resources (replace paths with actual file locations)
SPACESHIP_IMAGE = "spaceship_game_resources/spaceship.png"
ASTEROID_IMAGE = "spaceship_game_resources/asteroid.png"
CRYSTAL_IMAGE = "spaceship_game_resources/energy_crystal.png"
BACKGROUND_MUSIC = "spaceship_game_resources/background_music.wav"
CLASH_SOUND = "spaceship_game_resources/clash_sound.wav"
SUCCESS_SOUND = "spaceship_game_resources/clash_sound.wav"  # Assuming same for now

# Game initialization
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create game window
pygame.display.set_caption("Space Scavenger")  # Set window title
clock = pygame.time.Clock()  # Create clock object for controlling frame rate

# Load music and sounds
pygame.mixer.music.load(BACKGROUND_MUSIC)  # Load background music
pygame.mixer.music.play(-1)  # Loop the background music indefinitely
clash_sound = pygame.mixer.Sound(CLASH_SOUND)  # Load clash sound effect
success_sound = pygame.mixer.Sound(SUCCESS_SOUND)  # Load success sound effect

# Load images (spaceship, asteroid, crystal)
spaceship_img = pygame.image.load(SPACESHIP_IMAGE).convert_alpha()
asteroid_img = pygame.image.load(ASTEROID_IMAGE).convert_alpha()
crystal_img = pygame.image.load(CRYSTAL_IMAGE).convert_alpha()

# Resize images to appropriate sizes
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 48  # Define spaceship dimensions
spaceship_img = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))  # Scale spaceship image

# Player class (Spaceship)
class Spaceship:
    def __init__(self):
        self.image = spaceship_img  # Set spaceship image
        self.x = SCREEN_WIDTH // 2  # Initial x position (center of screen)
        self.y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10  # Initial y position (bottom of screen)
        self.speed = 8  # Speed of spaceship movement
        self.rect = self.image.get_rect(topleft=(self.x, self.y))  # Rect for collision detection

    def move(self, keys):
        # Move spaceship left or right based on key presses
        if keys[pygame.K_LEFT] and self.x > 0:  # Move left, ensure spaceship doesn't go off-screen
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - SPACESHIP_WIDTH:  # Move right
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)  # Update rect position

    def draw(self, screen):
        # Draw the spaceship on the screen at its current position
        screen.blit(self.image, (self.x, self.y))

# Falling object class (Asteroids and Crystals)
class FallingObject:
    def __init__(self, image, x, speed, size):
        self.image = pygame.transform.scale(image, size)  # Scale image to given size
        self.x = x  # Initial x position
        self.y = -size[1]  # Initial y position (off-screen at top)
        self.speed = speed  # Falling speed of the object
        self.rect = self.image.get_rect(topleft=(self.x, self.y))  # Rect for collision detection

    def move(self):
        # Move the falling object downwards
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)  # Update rect position

    def draw(self, screen):
        # Draw the falling object on the screen at its current position
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        # Check if the object has moved off the screen
        return self.y > SCREEN_HEIGHT

# Main game function
def main():
    # Game variables
    spaceship = Spaceship()  # Create a spaceship object
    asteroids = []  # List to store falling asteroids
    crystals = []  # List to store falling crystals
    score = 0  # Player's score
    level = 1  # Game level
    game_over = False  # Game over flag

    asteroid_timer = 0  # Timer for spawning asteroids
    crystal_timer = 0  # Timer for spawning crystals

    font = pygame.font.SysFont(None, 36)  # Font for displaying score and level

    # Main game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user quits the game
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()  # Get the state of all keys

        if not game_over:
            # Update spaceship position
            spaceship.move(keys)

            # Spawn asteroids at increasing speed as the level increases
            asteroid_timer += 1
            if asteroid_timer > max(30, 60 - level * 2):  # Faster spawn with increasing level
                asteroid_x = random.randint(0, SCREEN_WIDTH - 50)  # Random x position for asteroid
                asteroid_size = (50 + level * 2, 50 + level * 2)  # Increase asteroid size with level
                asteroids.append(FallingObject(asteroid_img, asteroid_x, 5 + level, asteroid_size))  # Create asteroid
                asteroid_timer = 0

            # Spawn crystals (slower rate)
            crystal_timer += 1
            if crystal_timer > 100:
                crystal_x = random.randint(0, SCREEN_WIDTH - 30)  # Random x position for crystal
                crystals.append(FallingObject(crystal_img, crystal_x, 5, (40, 40)))  # Create crystal
                crystal_timer = 0

            # Move and check for collisions
            for asteroid in asteroids[:]:
                asteroid.move()  # Move the asteroid down
                if spaceship.rect.colliderect(asteroid.rect):  # If spaceship collides with asteroid
                    clash_sound.play()  # Play collision sound
                    game_over = True  # End the game
                if asteroid.off_screen():  # Remove asteroid if it's off the screen
                    asteroids.remove(asteroid)

            for crystal in crystals[:]:
                crystal.move()  # Move the crystal down
                if spaceship.rect.colliderect(crystal.rect):  # If spaceship collects the crystal
                    success_sound.play()  # Play success sound
                    crystals.remove(crystal)  # Remove the crystal
                    score += 10  # Increase score
                    if score % 50 == 0:  # Increase level every 50 points
                        level += 1
                if crystal.off_screen():  # Remove crystal if it's off the screen
                    crystals.remove(crystal)

        # Draw everything on the screen
        screen.fill(WHITE)  # Fill the background with white
        spaceship.draw(screen)  # Draw the spaceship
        for asteroid in asteroids:
            asteroid.draw(screen)  # Draw each asteroid
        for crystal in crystals:
            crystal.draw(screen)  # Draw each crystal

        # Display score and level
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        # Display game over message
        if game_over:
            game_over_text = font.render("Game Over! Press Q to Quit.", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            if keys[pygame.K_q]:  # Quit the game if 'Q' is pressed
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)  # Control the frame rate

# Run the game
if __name__ == "__main__":
    main()
