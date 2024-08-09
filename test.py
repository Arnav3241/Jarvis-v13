import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

block_size = 10
font_style = pygame.font.SysFont(None, 25)


def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    gameDisplay.blit(value, [0, 0])


def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(gameDisplay, green, [
                         x[0], x[1], block_size, block_size])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    gameDisplay.blit(mesg, [display_width / 6, display_height / 3])


def game_loop():
    game_over = False
    game_close = False

    x1 = display_width / 2
    y1 = display_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    rand_x = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
    rand_y = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0

    while not game_over:

        while game_close:
            gameDisplay.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, red, [
                         rand_x, rand_y, block_size, block_size])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(block_size, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        if x1 == rand_x and y1 == rand_y:
            rand_x = round(random.randrange(
                0, display_width - block_size) / 10.0) * 10.0
            rand_y = round(random.randrange(
                0, display_height - block_size) / 10.0) * 10.0
            snake_length += 1

        clock.tick(30)

    pygame.quit()
    quit()


game_loop()
