import pygame
import time
import random

snake_speed = 15
counter = 0
warning = 50 # basically a counter 
# Window size
window_x = 200
window_y = 200
falling_squares = []
boss_battle = False
boss_battle_duration = 20  # Set the duration of the boss battle in frames
boss_battle_counter = 0
# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Snake Extreme')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50], [90, 50]]
# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0
level = 1

# displaying Score function
def show_score(choice, color, font, size):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()

    # displaying text
    game_window.blit(score_surface, score_rect)
def show_level(choice, color, font, size):
    # creating font object level_font
    level_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # level_surface
    level_surface = level_font.render('Level : ' + str(level), True, color)

    # create a rectangular object for the text
    # surface object
    level_rect = level_surface.get_rect()

    # set the position of the text
    level_rect.topright = (window_x - 10, 10)  # Adjust as needed

    # displaying text
    game_window.blit(level_surface, level_rect)
    
def reset_game():
    global direction, change_to, snake_position, snake_body, score, fruit_position, fruit_spawn, counter, window_x, window_y, level, warning
    direction = 'RIGHT'
    change_to = direction
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50]]
    score = 0
    level = 1
    fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
    fruit_spawn = True
    counter = 0
    warning = 50
    snake_speed = 15
    boss_battle = False
    # Reset window size back to 200x200 if it was doubled
    if window_x > 200 or window_y > 200:
        window_x = 200
        window_y = 200
        game_window = pygame.display.set_mode((window_x, window_y))
# game over function
def game_over():
    # Creating font objects
    my_font = pygame.font.SysFont('times new roman', 25)
    another_font = pygame.font.SysFont('times new roman', 15)

    # Creating text surfaces
    level_surface = my_font.render('Level : ' + str(level), True, red)
    quit_surface = another_font.render('ESC to Quit', True, red)
    restart_surface = another_font.render('ENTER to Restart', True, red)

    # Create rectangular objects for the text surfaces
    level_rect = level_surface.get_rect(midtop=(window_x / 2, window_y / 4))
    quit_rect = quit_surface.get_rect(midtop=(window_x / 2, window_y / 4 + 30))
    restart_rect = restart_surface.get_rect(midtop=(window_x / 2, window_y / 4 + 50))

    # Blit the text surfaces onto the screen
    game_window.blit(level_surface, level_rect)
    game_window.blit(quit_surface, quit_rect)
    game_window.blit(restart_surface, restart_rect)

    pygame.display.flip()

    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    restart = True
                    reset_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    # Clear the screen after restart
    game_window.fill(black)
    pygame.display.update()
    snake_speed = 15


# Game loop
while True:
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
        counter += 10
    if direction == 'DOWN':
        snake_position[1] += 10
        counter += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
        counter += 10
    if direction == 'RIGHT':
        snake_position[0] += 10
        counter += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        level += 1
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    # Set snake color based on the score
    snake_color = green  # default color

    # Check if the score is 10
    if score == 0:
        snake_speed = 15
        
    if score == 10:
        snake_speed = 15
        # Double the window size
        window_x *= 2
        window_y *= 2

        # Recenter the game window
        game_window = pygame.display.set_mode((window_x, window_y))
        snake_position = [window_x // 2, window_y // 2]
        score += 1  # Increment the score to avoid resizing the window continuously

    # Check if the score is 20
    if score == 21 or score ==31 :
        snake_speed = 15
        # Turn the screen green until certain key events occur
        if counter % 30 == 0:  # Change the condition to your preference
            game_window.fill(green)
            
    if score == 41 or score == 51:
        snake_speed = 25

    if score == 61 or score == 71:
        # Change snake color in a repeating pattern
        color_cycle = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 255)]
        snake_color = color_cycle[counter // 10 % len(color_cycle)]
        
    if score == 81 or score == 91:
        # Fruit moves locations every time the right key is clicked
        if event.key == pygame.K_RIGHT:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]

        # Display "Don't Turn Right!!!" in the middle of the screen
        font = pygame.font.SysFont('times new roman', 30)
        text = font.render("Don't Turn Right!!!", True, red)
        text_rect = text.get_rect(center=(window_x // 2, window_y // 2))
        game_window.blit(text, text_rect)
                
    if score == 101 or score == 111:
    # Decrease counter when a key is pressed
        font = pygame.font.SysFont('times new roman', 30)
        countdown_text = font.render(str(warning), True, red)
        countdown_rect = countdown_text.get_rect(center=(window_x // 2, window_y // 2))
        game_window.blit(countdown_text, countdown_rect)        
        if event.type == pygame.KEYDOWN:
                warning -= 1
    # Check if the counter has reached 0
        if warning <= -1:
            game_over()
            
    if score == 121 or score == 131 or score == 141:
        boss_battle = True
        boss_battle_counter += 1

        # Display "Boss Battle" in the middle of the screen
        font = pygame.font.SysFont('times new roman', 30)
        text = font.render("Boss Battle", True, red)
        text_rect = text.get_rect(center=(window_x // 2, window_y // 2))
        game_window.blit(text, text_rect)

        # Spawn falling red squares
        if boss_battle_counter % 10 == 0:  # Adjust the condition for the falling frequency
            square_size = 20
            square_color = red
            square_x = random.randrange(0, window_x - square_size + 1, square_size)
            square_y = 0  # Start from the top
            square_speed = 5  # Adjust the falling speed

            # Add the square to a list to manage multiple squares
            falling_squares.append([square_x, square_y, square_size, square_color, square_speed])

        # Update the positions of falling squares
        for square in falling_squares:
            square[1] += square[4]  # square[4] is the falling speed
            pygame.draw.rect(game_window, square[3], pygame.Rect(square[0], square[1], square[2], square[2]))

            # Check if the square collides with the snake
            if (
                snake_position[0] < square[0] + square[2]
                and snake_position[0] + 10 > square[0]
                and snake_position[1] < square[1] + square[2]
                and snake_position[1] + 10 > square[1]
            ):
               game_over()
            # Check if the square reached the bottom
            if square[1] >= window_y:
                falling_squares.remove(square)
                
    if score == 151:
    # Display "You Win" and "Congrats" on the screen
        win_font = pygame.font.SysFont('times new roman', 30)
        win_text = win_font.render("You Win", True, white)
        win_text_rect = win_text.get_rect(center=(window_x // 2, window_y // 2 - 30))
    
        congrats_font = pygame.font.SysFont('times new roman', 20)
        congrats_text = congrats_font.render("Congrats!", True, white)
        congrats_text_rect = congrats_text.get_rect(center=(window_x // 2, window_y // 2 + 10))
    
        game_window.blit(win_text, win_text_rect)
        game_window.blit(congrats_text, congrats_text_rect)

        pygame.display.flip()
        pygame.time.delay(5000)  # Delay for 5000 milliseconds (5 seconds)
        game_running = False  # Stop the game loop
        time.sleep(2)
        pygame.quit()
        quit() 
    for pos in snake_body:
        pygame.draw.rect(game_window, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    #show_score(1, white, 'times new roman', 20)
    show_level(1, white, 'times new roman', 20)
    

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
