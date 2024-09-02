import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pygame
import os
import random

# Initialize the Firebase app with your service account key
cred = credentials.Certificate('major.json')
firebaseDatabaseURl = os.getenv("firebaseDatabaseUrl")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://major-426c1-default-rtdb.firebaseio.com/"
})

# Reference to your database path
ref = db.reference('/')

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Coin Collector Game')

# Player attributes
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 2
player_direction = None

# Coin attributes
coin_width = 20
coin_height = 20
coin_x = random.randint(0, SCREEN_WIDTH - coin_width)
coin_y = 0
coin_speed = 4

# Score
score = 0
font = pygame.font.Font(None, 36)
flash_counter = 0

# Function to display score
def display_score():
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

# Function to display direction
def display_direction():
    global flash_counter
    direction_text = f"Direction: {player_direction.capitalize() if player_direction else 'Neutral'}"
    flash = flash_counter % 30 < 15  # Flash the text every half-second
    if flash:
        text = font.render(direction_text, True, RED)
        screen.blit(text, (10, 50))
    flash_counter += 1

# Function to move player
def move_player():
    global player_x
    if player_direction == 'left' and player_x > 0:
        player_x -= player_speed
    elif player_direction == 'right' and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

# Function to update the coin position
def update_coin():
    global coin_x, coin_y, score
    coin_y += coin_speed
    if coin_y > SCREEN_HEIGHT:
        coin_y = 0
        coin_x = random.randint(0, SCREEN_WIDTH - coin_width)

    # Check for collision with player
    if (player_x < coin_x < player_x + player_width or player_x < coin_x + coin_width < player_x + player_width) and (player_y < coin_y < player_y + player_height):
        score += 1
        coin_y = 0
        coin_x = random.randint(0, SCREEN_WIDTH - coin_width)

# Function to check for collision with boundaries
def check_collision():
    global running
    if player_x <= 0 or player_x >= SCREEN_WIDTH - player_width:
        running = False
        game_over()

# Function to display game over screen
def game_over():
    screen.fill(RED)
    text = font.render(f'Game Over! Score: {score}', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)
    reset_game()

# Function to reset the game
def reset_game():
    global player_x, player_y, coin_x, coin_y, score, player_direction, running
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - player_height - 10
    coin_x = random.randint(0, SCREEN_WIDTH - coin_width)
    coin_y = 0
    score = 0
    player_direction = None

    # Read the database again
    data = ref.get()
    if data:
        left_enabled = data.get('left', {}).get('enabled', False)
        right_enabled = data.get('right', {}).get('enabled', False)

        if left_enabled:
            player_direction = 'left'
        elif right_enabled:
            player_direction = 'right'

    running = True

# Listener function
def listener(event):
    global player_direction
    data = ref.get()
    if data:
        left_enabled = data.get('left', {}).get('enabled', False)
        right_enabled = data.get('right', {}).get('enabled', False)

        if left_enabled:
            player_direction = 'left'
        elif right_enabled:
            player_direction = 'right'
        else:
            player_direction = None

# Attach the listener to the reference
ref.listen(listener)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)

    # Move player
    move_player()

    # Update and draw coin
    update_coin()
    pygame.draw.rect(screen, YELLOW, (coin_x, coin_y, coin_width, coin_height))

    # Draw player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    # Display score
    display_score()

    # Display direction
    display_direction()

    # Check for collisions
    check_collision()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
