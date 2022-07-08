import pygame
WIDTH, HEIGHT = 900, 600
RES = WIDTH, HEIGHT
FPS = 60
screen = pygame.display.set_mode(RES)
pygame.display.set_caption("Pong")
RECT_LIST = [[60, HEIGHT//2 - 50, 15, 70], [WIDTH - 80, HEIGHT//2 - 50, 15, 70],
             [20, 20, 20, HEIGHT - 40], [20, HEIGHT - 40, WIDTH - 40, 20], [WIDTH - 40, 20, 20, HEIGHT - 40],
             [20, 20, WIDTH - 40, 20]]
circle_list_y = [40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560]


def handle_ball(ball, ball_x, ball_y, vel_x, vel_y):
    for i in range(len(RECT_LIST)):
        rect1 = pygame.Rect(RECT_LIST[0])
        rect2 = pygame.Rect(RECT_LIST[1])
        left_border = pygame.Rect(RECT_LIST[2])
        bottom_border = pygame.Rect(RECT_LIST[3])
        right_border = pygame.Rect(RECT_LIST[4])
        top_border = pygame.Rect(RECT_LIST[5])
        if ball.colliderect(rect1):
            vel_x = 2
        elif ball.colliderect(rect2):
            vel_x = -2
        elif ball.colliderect(left_border):
            vel_x = 2
        elif ball.colliderect(bottom_border):
            vel_y = -2
        elif ball.colliderect(right_border):
            vel_x = -2
        elif ball.colliderect(top_border):
            vel_y = 2
    return ball_x, ball_y, vel_x, vel_y


def keybinding():
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP] and RECT_LIST[1][1] > 40:
        RECT_LIST[1][1] -= 3
    if keys_pressed[pygame.K_DOWN] and RECT_LIST[1][1] < HEIGHT - 110:
        RECT_LIST[1][1] += 3
    if keys_pressed[pygame.K_w] and RECT_LIST[0][1] > 40:
        RECT_LIST[0][1] -= 3
    if keys_pressed[pygame.K_s] and RECT_LIST[0][1] < HEIGHT - 110:
        RECT_LIST[0][1] += 3


def make_win(ball_x, ball_y):
    for i in range(len(circle_list_y)):
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, circle_list_y[i]), 10)
    for rect in RECT_LIST:
        RECT = pygame.Rect(rect)
        pygame.draw.rect(screen, (255, 255, 255), RECT)
    ball = pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), 15)
    keybinding()
    pygame.display.update()
    return ball


def main():
    clock = pygame.time.Clock()
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2 - 50
    vel_x = 2
    vel_y = 2
    while True:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        ball_x += vel_x
        ball_y += vel_y
        ball = make_win(ball_x, ball_y)
        ball_x, ball_y, vel_x, vel_y = handle_ball(ball, ball_x, ball_y, vel_x, vel_y)
        pygame.display.update()


if __name__ == "__main__":
    main()
