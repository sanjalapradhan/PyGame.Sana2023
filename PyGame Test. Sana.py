import pygame
from pygame.locals import *
import random
import time

pygame.init()

screen_width = 600
screen_height = 600
cell_size = 20

# Colors of the items 
bg = (255, 200, 150)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
food_col = (200, 50, 50)
blue = (0, 0, 255)
red = (255, 0, 0)

# variables
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont(None, 40)
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)
snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
direction = 1
update_snake = 0
food = [0, 0]
new_food = True
new_piece = [0, 0]
game_over = False
clicked = False
score = 0

# Function to initialize the game statee
def initialize_game_state():
    global snake_pos, direction, update_snake, food, new_food, new_piece, game_over, clicked, score
    snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
    direction = 1
    update_snake = 0
    food = [0, 0]
    new_food = True
    new_piece = [0, 0]
    game_over = False
    clicked = False
    score = 0

# stimulating user inputs to the function 
def simulate_user_input(key):
    pygame.event.post(pygame.event.Event(KEYDOWN, {'key': key}))

# Function to test player movements
def test_player_movement():
    initialize_game_state()

    simulate_user_input(pygame.K_UP)
    assert snake_pos[0][1] == snake_pos[1][1] - cell_size

    simulate_user_input(pygame.K_DOWN)
    assert snake_pos[0][1] == snake_pos[1][1] + cell_size

    simulate_user_input(pygame.K_RIGHT)
    assert snake_pos[0][0] == snake_pos[1][0] + cell_size

    simulate_user_input(pygame.K_LEFT)
    assert snake_pos[0][0] == snake_pos[1][0] - cell_size

    print("Player movement tests passed.")


# Function to draw the game screen
def draw_screen():
    screen.fill(bg)

# Function to draw the player's score
def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0, 0))

# Function to check if the game is over
def check_game_over():
    head_count = 0
    for x in snake_pos:
        if snake_pos[0] == x and head_count > 0:
            return True
        head_count += 1

    if ( snake_pos[0][0] < 0
        or snake_pos[0][0] > screen_width
        or snake_pos[0][1] < 0
        or snake_pos[0][1] > screen_height):
        return True

    return False

# Function to draw the game over screen
def draw_game_over():
    over_text = "Game Over!"
    over_img = font.render(over_text, True, blue)
    pygame.draw.rect(screen, red, (screen_width // 4, screen_height // 2 - 60, screen_width // 2, 50))
    screen.blit(over_img, (screen_width // 4, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

# Function to update the snake's position
def update_snake_position():
    global game_over, update_snake

    if not game_over:
        if update_snake > 5:
            update_snake = 0
            snake_pos.insert(0, list(snake_pos[0]))
            if direction == 1:
                snake_pos[0][1] -= cell_size
            elif direction == 3:
                snake_pos[0][1] += cell_size
            elif direction == 2:
                snake_pos[0][0] += cell_size
            elif direction == 4:
                snake_pos[0][0] -= cell_size

            game_over = check_game_over()

# Function to handle the main game loop
def game_loop():
    global run, game_over, update_snake, food, new_food, new_piece, clicked, score, snake_pos, direction

    while run:
        draw_screen()
        draw_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                handle_key_press(event.key)

        create_food()
        draw_food()

        if snake_pos[0] == food:
            handle_food_eaten()

        update_snake_position()

        if game_over:
            draw_game_over()
            handle_game_over_click()

        draw_snake()
        pygame.display.update()

        time.sleep(0.03)  # Further decreased delay for faster gameplay

        update_snake += 1

    pygame.quit()

# Function to handle key presses during the game
def handle_key_press(key):
    global direction

    if key == pygame.K_UP and direction != 3:
        direction = 1
    elif key == pygame.K_RIGHT and direction != 4:
        direction = 2
    elif key == pygame.K_DOWN and direction != 1:
        direction = 3
    elif key == pygame.K_LEFT and direction != 2:
        direction = 4

# Function to create new food
def create_food():
    global new_food, food

    if new_food:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width // cell_size) - 1)
        food[1] = cell_size * random.randint(0, (screen_height // cell_size) - 1)

# Function to draw the food on the screen
def draw_food():
    pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))

# Function to handle actions when the snake eats the food
def handle_food_eaten():
    global new_food, new_piece, score

    new_food = True
    new_piece = list(snake_pos[-1])

    if direction == 1:
        new_piece[1] += cell_size
    elif direction == 3:
        new_piece[1] -= cell_size
    elif direction == 2:
        new_piece[0] -= cell_size
    elif direction == 4:
        new_piece[0] += cell_size

    snake_pos.append(new_piece)
    score += 1

# Function to handle actions when the game is over and the player clicks
def handle_game_over_click():
    global game_over, update_snake, food, new_food, new_piece, clicked, score, snake_pos, direction

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if (
        again_rect.left < mouse_x < again_rect.right
        and again_rect.top < mouse_y < again_rect.bottom
    ):
        if pygame.mouse.get_pressed()[0]:
            initialize_game_state()

# Function to draw the snake on the screen
def draw_snake():
    for segment in snake_pos:
        pygame.draw.rect(screen, body_outer, (segment[0], segment[1], cell_size, cell_size))
        pygame.draw.rect(screen, body_inner, (segment[0] + 1, segment[1] + 1, cell_size - 2, cell_size - 2))

# Run the game loop
run = True
game_loop()
