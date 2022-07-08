import pygame
import datetime
import random
WIDTH, HEIGHT = 900, 600
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
x_list = [0, 33, 66, 99, 132, 165, 198, 231, 264, 297, 330, 363, 396, 429, 462, 495, 528,
          561, 594, 627, 660, 693, 726, 759, 792, 825, 858]
y_list = [0, 33, 66, 99, 132, 165, 198, 231, 264, 297, 330, 363, 396, 429, 462, 495, 528, 561]
move_per_second = 313
FPS = 60
grid_list = []
for x in x_list:
    for y in y_list:
        grid_list.append([x + 5, y + 5])


def end_screen(text, score):
    end_font = pygame.font.SysFont("Corbel", 100)
    lose_text = end_font.render(text, True, (0, 0, 0))
    score_text = end_font.render(f"Score: {score}", True, (0, 0, 0))
    restart_text = end_font.render("Restart", True, (0, 0, 0))
    restart_rect = pygame.Rect(250, 300, restart_text.get_width(), restart_text.get_height())
    while True:
        mouse = pygame.mouse.get_pos()
        screen.fill((50, 50, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(mouse):
                    main()
        if restart_rect.collidepoint(mouse):
            pygame.draw.rect(screen, (100, 100, 100), restart_rect)
        screen.blit(lose_text, (250, 200))
        screen.blit(restart_text, (250, 300))
        screen.blit(score_text, (250, 100))
        pygame.display.update()


def grid():
    screen.fill((50, 50, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        for i in grid_list:
            rect = pygame.Rect(i[0], i[1] - 33, 30, 30)
            pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.display.update()


def food(snake_list):
    rect = None
    try:
        food_x = grid_list[random.randint(0, len(grid_list) - 1)][0]
        food_y = grid_list[random.randint(0, len(grid_list) - 1)][1]
        if [food_x, food_y] in snake_list:
            raise StopIteration
        else:
            rect = pygame.Rect(food_x, food_y, 30, 30)
    except StopIteration:
        food(snake_list)
    return rect


def main():
    snake_list = [grid_list[len(grid_list)//2 - 2]]
    clock = pygame.time.Clock()
    key_pressed = ""
    spawn = True
    score = 0
    food_rect = food(snake_list)
    while True:
        clock.tick(15)
        screen.fill((70, 70, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and key_pressed != "s":
                    key_pressed = "w"
                if event.key == pygame.K_DOWN and key_pressed != "w":
                    key_pressed = "s"
                if event.key == pygame.K_LEFT and key_pressed != "d":
                    key_pressed = "a"
                if event.key == pygame.K_RIGHT and key_pressed != "a":
                    key_pressed = "d"
                if event.key == pygame.K_g:
                    snake_list.append(grid_list[grid_list.index([snake_list[-1][0] + 33, snake_list[-1][1]])])
                if event.key == pygame.K_h:
                    snake_list.append(grid_list[grid_list.index(snake_list[-1]) + 1])
        for snake in snake_list:
            snake_rect = pygame.Rect(snake[0], snake[1], 30, 30)
            pygame.draw.rect(screen, (0, 0, 0), snake_rect)
        if spawn:
            try:
                pygame.draw.rect(screen, (100, 100, 100), food_rect)
            except TypeError:
                food_rect = food(snake_list)
                continue
        if key_pressed == "w":
            if [snake_list[0][0], snake_list[0][1] - 33] in grid_list:
                snake_list.insert(0, grid_list[grid_list.index([snake_list[0][0], snake_list[0][1] - 33])])
                snake_list.remove(snake_list[-1])
            else:
                snake_list.insert(0, grid_list[grid_list.index([snake_list[0][0], grid_list[-1][1]])])
                snake_list.remove(snake_list[-1])
        elif key_pressed == "s":
            if [snake_list[0][0], snake_list[0][1] + 33] in grid_list:
                snake_list.insert(0, grid_list[grid_list.index([snake_list[0][0], snake_list[0][1] + 33])])
                snake_list.remove(snake_list[-1])
            else:
                snake_list.insert(0, grid_list[grid_list.index([snake_list[0][0], grid_list[0][1]])])
                snake_list.remove(snake_list[-1])
        elif key_pressed == "a":
            if [snake_list[0][0] - 33, snake_list[0][1]] in grid_list:
                snake_list.insert(0, grid_list[grid_list.index([snake_list[0][0] - 33, snake_list[0][1]])])
                snake_list.remove(snake_list[-1])
            else:
                snake_list.insert(0, grid_list[grid_list.index([grid_list[-1][0], snake_list[0][1]])])
                snake_list.remove(snake_list[-1])
        elif key_pressed == "d":
            if [snake_list[0][0] + 33, snake_list[0][1]] in grid_list:
                snake_list.insert(0, grid_list[grid_list.index([snake_list[0][0] + 33, snake_list[0][1]])])
                snake_list.remove(snake_list[-1])
            else:
                snake_list.insert(0, grid_list[grid_list.index([grid_list[0][0], snake_list[0][1]])])
                snake_list.remove(snake_list[-1])
        if snake_list.count(snake_list[0]) > 1:
            snake_list.remove(snake_list[0])
            end_screen("You Lose", score)
        if pygame.Rect(snake_list[0][0], snake_list[0][1], 30, 30).colliderect(food_rect):
            score += 1
            if key_pressed == "w" or "s":
                try:
                    if grid_list[grid_list.index(snake_list[-1]) + 1] in grid_list:
                        snake_list.append(grid_list[grid_list.index([snake_list[-1][0] + 33, snake_list[-1][1]])])
                except IndexError:
                    pass
                except ValueError:
                    pass
            elif key_pressed == "a" or key_pressed == "d":
                try:
                    if grid_list[grid_list.index([snake_list[-1][0] + 33, snake_list[-1][1]])] in grid_list:
                        snake_list.append(grid_list[grid_list.index(snake_list[-1]) + 1])
                except IndexError:
                    pass
                except ValueError:
                    pass
            food_rect = food(snake_list)
        pygame.display.update()

def timer(func):
    now = datetime.datetime.now()
    func()
    later = datetime.datetime.now()
    return later - now


if __name__ == '__main__':
    main()
