import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Load resources
# Replace these paths with your actual file locations in "spaceship_game_resources"
SPACESHIP_IMAGE = "spaceship_game_resources/spaceship.png"
ASTEROID_IMAGE = "spaceship_game_resources/asteroid.png"
CRYSTAL_IMAGE = "spaceship_game_resources/energy_crystal.png"
BACKGROUND_MUSIC = "spaceship_game_resources/background_music.wav"
CLASH_SOUND = "spaceship_game_resources/clash_sound.wav"
SUCCESS_SOUND = "spaceship_game_resources/clash_sound.wav"  # Assuming same for now

# Game initialization
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Scavenger")
clock = pygame.time.Clock()

# Load music and sounds
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)  # Loop the background music
clash_sound = pygame.mixer.Sound(CLASH_SOUND)
success_sound = pygame.mixer.Sound(SUCCESS_SOUND)

# Load images
spaceship_img = pygame.image.load(SPACESHIP_IMAGE).convert_alpha()
asteroid_img = pygame.image.load(ASTEROID_IMAGE).convert_alpha()
crystal_img = pygame.image.load(CRYSTAL_IMAGE).convert_alpha()

# Resize images
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 48
spaceship_img = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Player class
class Spaceship:
    def __init__(self):
        self.image = spaceship_img
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
        self.speed = 8
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - SPACESHIP_WIDTH:
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Falling object class
class FallingObject:
    def __init__(self, image, x, speed, size):
        self.image = pygame.transform.scale(image, size)
        self.x = x
        self.y = -size[1]
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

# Main game function
def main():
    # Game variables
    spaceship = Spaceship()
    asteroids = []
    crystals = []
    score = 0
    level = 1
    game_over = False

    asteroid_timer = 0
    crystal_timer = 0

    font = pygame.font.SysFont(None, 36)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            # Update spaceship
            spaceship.move(keys)

            # Spawn asteroids
            asteroid_timer += 1
            if asteroid_timer > max(30, 60 - level * 2):  # Faster spawn with levels
                asteroid_x = random.randint(0, SCREEN_WIDTH - 50)
                asteroid_size = (50 + level * 2, 50 + level * 2)
                asteroids.append(FallingObject(asteroid_img, asteroid_x, 5 + level, asteroid_size))
                asteroid_timer = 0

            # Spawn crystals
            crystal_timer += 1
            if crystal_timer > 100:  # Crystals spawn slower
                crystal_x = random.randint(0, SCREEN_WIDTH - 30)
                crystals.append(FallingObject(crystal_img, crystal_x, 5, (40, 40)))
                crystal_timer = 0

            # Move and check collisions
            for asteroid in asteroids[:]:
                asteroid.move()
                if spaceship.rect.colliderect(asteroid.rect):
                    clash_sound.play()
                    game_over = True
                if asteroid.off_screen():
                    asteroids.remove(asteroid)

            for crystal in crystals[:]:
                crystal.move()
                if spaceship.rect.colliderect(crystal.rect):
                    success_sound.play()
                    crystals.remove(crystal)
                    score += 10
                    if score % 50 == 0:
                        level += 1  # Increase level every 50 points
                if crystal.off_screen():
                    crystals.remove(crystal)

        # Draw everything
        screen.fill(WHITE)
        spaceship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for crystal in crystals:
            crystal.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        if game_over:
            game_over_text = font.render("Game Over! Press Q to Quit.", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()
