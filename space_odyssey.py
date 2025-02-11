
import pygame
import random

# Initialize pygame
pygame.init()

# Constants
info = pygame.display.Info()
WIDTH, HEIGHT = int(info.current_w * 0.8), int(info.current_h * 0.8)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font("fonts/SixtyfourConvergence-Regular.ttf", 36)


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(" Space Odyssey ")

MENU_BUTTON_RECT = pygame.Rect(screen.get_width() - 130, 10, 120, 40) 
MENU_RECT = pygame.Rect(0, 0, 400, 300)  
MENU_RECT.center = (WIDTH // 2, HEIGHT // 2) 
RESUME_BUTTON_RECT = pygame.Rect(0, 0, 200, 50)
QUIT_BUTTON_RECT = pygame.Rect(0, 0, 200, 50)
RESUME_BUTTON_RECT.center = (MENU_RECT.centerx, MENU_RECT.top + 100)
QUIT_BUTTON_RECT.center = (MENU_RECT.centerx, MENU_RECT.top + 180)


# Loading assets
player_img = pygame.image.load("images/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
asteroid_imgs = [pygame.image.load(f"images/asteroid{i}.png") for i in range(1, 4)]
for i in range(len(asteroid_imgs)):
    asteroid_imgs[i] = pygame.transform.scale(asteroid_imgs[i], (50 + i * 20, 50 + i * 20))


# Star class for twinkling effect
class Star:
    def __init__(self, WIDTH, HEIGHT):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 2
        self.opacity = random.uniform(0.2, 1.0)
        self.twinkle_speed = random.uniform(0.02, 0.05)

    def update(self, WIDTH, HEIGHT):
        self.opacity += self.twinkle_speed
        if self.opacity >= 1.0 or self.opacity <= 0.2:
            self.twinkle_speed = -self.twinkle_speed
        self.y += 1
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, screen):
        a = int(self.opacity * 255)
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surface.fill((255, 255, 255, ))
        screen.blit(surface, (self.x, self.y))

# Create stars and When screen resizes, regenerate stars
NUM_STARS = 250
stars = [Star(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_STARS)]

# Function to reset the game
def reset_game():
    global player_x, player_y, bullets, asteroids, score
    player_x, player_y = WIDTH // 2, HEIGHT - 70
    bullets = []
    asteroids = []
    for _ in range(5):
        create_asteroid()
    score = 0

# Player settings
player_speed = 5

# Bullets
bullets = []
bullet_speed = 7

# Asteroids
asteroids = []
def create_asteroid():
    size_index = random.randint(0, 2)
    asteroid_x = random.randint(0, WIDTH - 70)
    asteroid_y = random.randint(-150, -50)
    asteroid_speed = random.randint(2, 5)
    health = size_index + 1  # Bigger asteroids are going to take more hits
    asteroids.append([asteroid_x, asteroid_y, asteroid_speed, size_index, health])

# Function to check collision
def check_collision(player_x, player_y, asteroids):
    for asteroid in asteroids:
        if (player_x < asteroid[0] + (50 + asteroid[3] * 20) and player_x + 50 > asteroid[0] and
            player_y < asteroid[1] + (50 + asteroid[3] * 20) and player_y + 50 > asteroid[1]):
            return True
    return False

# Function to show start screen
def show_start_screen():
    screen.fill(BLACK)
    title_text = FONT.render(" SPACE ODYSSEY ", True, RED)
    start_text = FONT.render("Press ENTER to Start", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Global variable to maintain the highest score
highest_score = 0

# Function to show game over screen
def show_game_over_screen(score):
    global highest_score

    # Update the highest score if the current score is higher
    if score > highest_score:
        highest_score = score

    screen.fill(BLACK)
    game_over_text = FONT.render("GAME OVER!", True, RED)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    high_score_text = FONT.render(f"Highest Score: {highest_score}", True, WHITE)
    restart_text = FONT.render("Press ENTER to Restart or ESC to Quit", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.8))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(high_score_text, high_score_rect)
    screen.blit(restart_text, restart_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def draw_menu():
    pygame.draw.rect(screen, RED, (WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2), border_radius=10)
    resume_text = FONT.render("Resume", True, RED)
    resume_text_rect = resume_text.get_rect(center=RESUME_BUTTON_RECT.center)
    quit_text = FONT.render("Quit", True, RED)
    quit_text_rect = quit_text.get_rect(center=QUIT_BUTTON_RECT.center)
    pygame.draw.rect(screen, BLACK, RESUME_BUTTON_RECT, border_radius=10)  
    pygame.draw.rect(screen, BLACK, QUIT_BUTTON_RECT, border_radius=10)  
    screen.blit(resume_text, resume_text_rect)  
    screen.blit(quit_text, quit_text_rect)   

def draw_menu_button():
    menu_text = FONT.render("Menu", True, RED)
    menu_text_rect = menu_text.get_rect(center=MENU_BUTTON_RECT.center)
    pygame.draw.rect(screen, BLACK, MENU_BUTTON_RECT, border_radius=10)  # Draw button with rounded corners
    screen.blit(menu_text, menu_text_rect)  # Place text at the center



# Main game function
def main_game():
    global player_x, player_y, bullets, asteroids, score, screen, HEIGHT, WIDTH
    reset_game()

    running = True
    paused = False
    while running:
        screen.fill(BLACK)
        draw_menu_button()

        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h  # Update the new width and height
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                MENU_BUTTON_RECT.topleft = (screen.get_width() - 130, 10)  # Adjust position dynamically
                RESUME_BUTTON_RECT.topleft = (MENU_RECT.centerx - 100, MENU_RECT.top + 80)
                QUIT_BUTTON_RECT.topleft = (MENU_RECT.centerx - 100, MENU_RECT.top + 160)

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_x + 22, player_y])
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'Esc' to toggle pause
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
            
                if MENU_BUTTON_RECT.collidepoint(mouse_pos):  # Click menu button
                    paused = True
            
                if paused:  # Handle clicks only when paused
                    if RESUME_BUTTON_RECT.collidepoint(mouse_pos):  # Click Resume
                        paused = False
                    elif QUIT_BUTTON_RECT.collidepoint(mouse_pos):  # Click Quit
                        running = False

        if paused:
            draw_menu()  # Show the pause menu
        
        # Update and draw stars
        for star in stars:
            star.update(WIDTH, HEIGHT)
            star.draw(screen)
        
        # Event handling
            


            
        if(not paused):
        # Get keys pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
                player_y += player_speed
            
            # Move bullets
            for bullet in bullets[:]:
                bullet[1] -= bullet_speed
                if bullet[1] < 0:
                    bullets.remove(bullet)
            
            # Move asteroids
            for asteroid in asteroids[:]:
                asteroid[1] += asteroid[2]
                if asteroid[1] > HEIGHT:
                    asteroids.remove(asteroid)
                    create_asteroid()
            
            # Bullet collision
            for bullet in bullets[:]:
                for asteroid in asteroids[:]:
                    ax, ay, _, size_index, health = asteroid
                    if ax < bullet[0] < ax + (50 + size_index * 20) and ay < bullet[1] < ay + (50 + size_index * 20):
                        asteroid[4] -= 1  # Reduce health
                        bullets.remove(bullet)
                        if asteroid[4] <= 0:
                            asteroids.remove(asteroid)
                            score += 10
                            create_asteroid()
                        break
            
            # Check collision with player
            if check_collision(player_x, player_y, asteroids):
                running = False

            # Draw player
            screen.blit(player_img, (player_x, player_y))
            
            # Draw bullets
            for bullet in bullets:
                pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 5, 10))
            
            # Draw asteroids
            for asteroid in asteroids:
                screen.blit(asteroid_imgs[asteroid[3]], (asteroid[0], asteroid[1]))
            
            # Display score
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
            
            # Update display
        pygame.display.update()
        pygame.time.delay(30)
    
    return score

# Run the game loop
while True:
    show_start_screen()
    final_score = main_game()
    show_game_over_screen(final_score)
