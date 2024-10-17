#Program of 2D game
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()  # Get screen dimensions
pygame.display.set_caption("Elden Ring Spaceship Edition ~Priyanshu Mitra")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load space background and scale it
space_background = pygame.image.load("C:/Users/PRIYANSHU MITRA/Downloads/realistic-galaxy-background/5532919.jpg")
space_background = pygame.transform.scale(space_background, (screen_width, screen_height))

# Load spaceship images and scale them
player_image = pygame.image.load("C:/Users/PRIYANSHU MITRA/Downloads/png-transparent-spaceshipone-spaceshiptwo-sprite-spacecraft-two-dimensional-space-spaceship-game-fictional-character-space-removebg-preview.jpg")
player_size = int(screen_height * 0.1)  # Set spaceship size to 10% of screen height
player_image = pygame.transform.scale(player_image, (player_size, player_size))

enemy_image = pygame.image.load("C:/Users/PRIYANSHU MITRA/Downloads/png-transparent-sprite-opengameart-org-millionth-2d-computer-graphics-space-invaders-game-spacecraft-star-wars-episode-vii-thumbnail-removebg-preview.jpg")
enemy_image = pygame.transform.scale(enemy_image, (int(screen_height * 0.1), int(screen_height * 0.1)))  # Scale enemy size

# Load ammo image and scale it
bullet_image = pygame.image.load("C:/Users/PRIYANSHU MITRA/Downloads/WhatsApp Image 2024-10-17 at 23.02.00_18a914c8.jpg")
bullet_size = int(screen_height * 0.025)  # Set bullet size to 2.5% of screen height
bullet_image = pygame.transform.scale(bullet_image, (bullet_size, bullet_size))

# Load sounds and music
pygame.mixer.music.load("C:/Users/PRIYANSHU MITRA/Downloads/3-34. Godfrey, First Elden Lord.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely
jump_sound = pygame.mixer.Sound("C:/Users/PRIYANSHU MITRA/Downloads/3-34. Godfrey, First Elden Lord.mp3")
shoot_sound = pygame.mixer.Sound("C:/Users/PRIYANSHU MITRA/Downloads/3-34. Godfrey, First Elden Lord.mp3")
game_over_sound = pygame.mixer.Sound("C:/Users/PRIYANSHU MITRA/Downloads/3-34. Godfrey, First Elden Lord.mp3")

# Set up initial player properties
player_pos = pygame.Rect(screen_width // 2 - player_size // 2, screen_height - player_size - 20, player_size, player_size)  # Centered at the bottom
player_speed = 5
player_jump = False
gravity = 1
jump_height = 15
jump_velocity = 0

# Enemy properties
enemies = [pygame.Rect(random.randint(0, screen_width - int(screen_height * 0.1)), random.randint(-100, -50), int(screen_height * 0.1), int(screen_height * 0.1)) for _ in range(5)]
enemy_speed = 2

# Bullet properties
bullets = []
bullet_speed = 7

# Health points (HP)
player_hp = 3

# Scoring system
score = 0
font_size = int(screen_height * 0.05)  # Set font size to 5% of screen height
font = pygame.font.Font(None, font_size)

# Levels and game status
level = 1
game_over = False
in_home_screen = True  # Flag for home screen

# Set up the clock for frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    if in_home_screen:
        # Draw space background on home screen
        screen.blit(space_background, (0, 0))
        
        # Home screen with control instructions
        title_text = font.render("  Welcome to Elden Ring Spaceship Edition", True, WHITE)
        instructions = [
            " ",
            "                                         ~Priyanshu Mitra",
            " ",
            "About Controls :-",
            " ",
            "Move Left : Arrow Left Key",
            "  ",
            "Move Right : Arrow Right Key",
            " ",
            "Jump : Space Key",
            " ",
            "Shoot : S Key",
            " ",
            "Press Enter to Start"
        ]
        screen.blit(title_text, (screen_width // 4, screen_height // 4))
        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, WHITE)
            screen.blit(instruction_text, (screen_width // 3, screen_height // 4 + 30 + i * 30))

        pygame.display.flip()

        # Handle events on the home screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game on Enter
                    in_home_screen = False  # Exit home screen

    else:
        # Draw space background in the game
        screen.blit(space_background, (0, 0))

        if game_over:
            # Display Game Over and final score
            game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
            screen.blit(game_over_text, (screen_width // 4, screen_height // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Jumping
                if event.key == pygame.K_SPACE and not player_jump:
                    player_jump = True
                    jump_velocity = -jump_height
                    jump_sound.play()
                
                # Shooting (press S key to shoot)
                if event.key == pygame.K_s:
                    if len(bullets) < 5:  # Limit bullets on screen
                        bullets.append(pygame.Rect(player_pos.centerx - bullet_size // 2, player_pos.y, bullet_size, bullet_size))
                        shoot_sound.play()

        # Handle movement
        keys = pygame.key.get_pressed()

        # Left and Right movement
        if keys[pygame.K_LEFT] and player_pos.left > 0:
            player_pos.x -= player_speed
        if keys[pygame.K_RIGHT] and player_pos.right < screen_width:
            player_pos.x += player_speed

        # Apply gravity and handle jumping
        if player_jump:
            player_pos.y += jump_velocity
            jump_velocity += gravity
            if player_pos.bottom >= screen_height:
                player_pos.bottom = screen_height
                player_jump = False

        # Bullet movement and enemy collision
        bullets_to_remove = []  # List to keep track of bullets to remove

        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets_to_remove.append(bullet)  # Mark bullet for removal
            else:
                for enemy in enemies:
                    if bullet.colliderect(enemy):
                        bullets_to_remove.append(bullet)  # Mark bullet for removal
                        enemies.remove(enemy)
                        enemies.append(pygame.Rect(random.randint(0, screen_width - int(screen_height * 0.1)), random.randint(-100, -50), int(screen_height * 0.1), int(screen_height * 0.1)))
                        score += 20

        # Remove bullets that are marked for removal
        for bullet in bullets_to_remove:
            if bullet in bullets:  # Check if bullet still exists in the list
                bullets.remove(bullet)

        # Enemy movement and player collision
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > screen_height:
                enemy.x = random.randint(0, screen_width - enemy.width)
                enemy.y = -enemy.height
                score += 10  # Increase score when an enemy is avoided
            if player_pos.colliderect(enemy):
                player_hp -= 1  # Decrease HP on collision
                enemies.remove(enemy)
                enemies.append(pygame.Rect(random.randint(0, screen_width - int(screen_height * 0.1)), random.randint(-100, -50), int(screen_height * 0.1), int(screen_height * 0.1)))
                if player_hp <= 0:
                    game_over_sound.play()
                    game_over = True  # End the game when HP reaches 0

        # Draw player, enemies, and bullets (with ammo image)
        screen.blit(player_image, player_pos)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)

        # Display the score and HP
        score_text = font.render(f"Score: {score}", True, WHITE)
        hp_text = font.render(f"HP: {player_hp}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(hp_text, (10, 40))

        # Level progression
        if score > level * 100:
            level += 1
            enemy_speed += 1  # Increase difficulty with higher levels
            enemies.append(pygame.Rect(random.randint(0, screen_width - int(screen_height * 0.1)), random.randint(-100, -50), int(screen_height * 0.1), int(screen_height * 0.1)))  # Add new enemies as level increases

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Quit the game
pygame.quit()


