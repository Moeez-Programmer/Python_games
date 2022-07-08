import pygame
import os

# from particle_system import Particles

WIDTH, HEIGHT = 900, 600
RES = (WIDTH, HEIGHT)
ENEMY_VEL = 1
WHITE = (255, 255, 255)
VEL = 6
FIRE_VEL = 10
FPS = 60
first_row_x = 100
first_grid_y = 30
second_grid_y = 110
third_grid_y = 190
fourth_grid_y = 270
fifth_grid_y = 350
ENEMY_LIST_STAGE1 = [(first_row_x, first_grid_y), (first_row_x, second_grid_y), (first_row_x, third_grid_y),
                     (first_row_x, fourth_grid_y), (first_row_x, fifth_grid_y),
                     (first_row_x * 2, first_grid_y), (first_row_x * 2, second_grid_y), (first_row_x * 2, third_grid_y),
                     (first_row_x * 2, fourth_grid_y), (first_row_x * 2, fifth_grid_y),
                     (first_row_x * 3, first_grid_y), (first_row_x * 3, second_grid_y), (first_row_x * 3, third_grid_y),
                     (first_row_x * 3, fourth_grid_y), (first_row_x * 3,
                                                        fifth_grid_y),
                     (first_row_x * 4, first_grid_y), (first_row_x * 4, second_grid_y), (first_row_x * 4, third_grid_y),
                     (first_row_x * 4, fourth_grid_y), (first_row_x * 4,
                                                        fifth_grid_y),
                     (first_row_x * 5, first_grid_y), (first_row_x * 5, second_grid_y), (first_row_x * 5, third_grid_y),
                     (first_row_x * 5, fourth_grid_y), (first_row_x * 5,
                                                        fifth_grid_y),
                     (first_row_x * 6, first_grid_y), (first_row_x * 6, second_grid_y), (first_row_x * 6, third_grid_y),
                     (first_row_x * 6, fourth_grid_y), (first_row_x * 6,
                                                        fifth_grid_y),
                     (first_row_x * 7, first_grid_y), (first_row_x * 7, second_grid_y), (first_row_x * 7, third_grid_y),
                     (first_row_x * 7, fourth_grid_y), (700, fifth_grid_y)]
enemies_no = len(ENEMY_LIST_STAGE1)
pygame.init()
pygame.font.init()
pygame.mixer.init()
# HIT_PARTICLE = Particles((125,125,125), 100, 1, 0.02, 10)
screen = pygame.display.set_mode(RES)
GLOBAL_PATH = "Assets"
GAME_FONT = pygame.font.SysFont("Corbel", 100)
SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT = (75, 50)
SPACE_SHIP_YELLOW_IMAGE = pygame.image.load(os.path.join(GLOBAL_PATH, "spaceship_yellow.png"))
SPACE_SHIP_YELLOW = pygame.transform.rotate(pygame.transform.scale(SPACE_SHIP_YELLOW_IMAGE,
                                                                   (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)), 180)
SPACE_SHIP_RED_IMAGE = pygame.image.load(os.path.join(GLOBAL_PATH, "spaceship_red.png"))
SPACE_SHIP_RED = pygame.transform.scale(SPACE_SHIP_RED_IMAGE, (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join(GLOBAL_PATH, "space.png")), (WIDTH, HEIGHT))
RED_HIT = pygame.USEREVENT
# BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(GLOBAL_PATH, "Gun+Silencer.mp3"))
# BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(GLOBAL_PATH, "Grenade+1.mp3"))
# BACKGROUND = pygame.mixer.Sound(os.path.join(GLOBAL_PATH, "background.mp3"))
pygame.display.set_caption("Space Invaders")
enemy_velx = 2
enemy_vely = 20
enemy_x = []
enemy_y = []
enemy_health = []
enemy_x_change = []
enemy_y_change = []

for i in range(enemies_no):
    enemy_x.append(ENEMY_LIST_STAGE1[i][0])
    enemy_y_change.append(20)
    enemy_y.append(ENEMY_LIST_STAGE1[i][1])
    enemy_health.append(5)
    enemy_x_change.append(1)


# def handle_bullets(bullets, enemy_X, enemy_Y):


def keybinding(player, bullets):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and player.x - VEL > 0:  # Left
        player.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and player.x + VEL < WIDTH - player.width:  # Right
        player.x += VEL
    if keys_pressed[pygame.K_UP] and player.y - VEL > 0:  # UP
        player.y -= VEL
    if keys_pressed[pygame.K_DOWN] and player.y + VEL < HEIGHT - player.height:  # Down
        player.y += VEL


def end_screen(text):
    lose_text = GAME_FONT.render(text, True, (0, 255, 0))
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(SPACE, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.blit(SPACE, (0, 0))
        screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() + 170, HEIGHT // 2 - lose_text.get_height() + 30))
        pygame.display.update()


def iscollision(enemy_X, enemy_Y, bullet_X, bullet_Y):
    player = pygame.Rect(enemy_X, enemy_Y, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
    red = pygame.Rect(bullet_X, bullet_Y, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
    if player.colliderect(red):
        end_screen("You Lose!")
    distance = ((bullet_X - enemy_X) ** 2 + (bullet_Y - enemy_Y) ** 2) ** 1 / 2
    if distance <= SPACE_SHIP_WIDTH:
        return True
    else:
        return False


def main():
    # red_health = 10
    # hit_dict = {}
    player = pygame.Rect(WIDTH // 2 - SPACE_SHIP_WIDTH, HEIGHT - SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
    bullets = []
    # BACKGROUND.play()
    # particles = [HIT_PARTICLE.make_particle((200, ),(200, ))]
    while True:
        screen.blit(SPACE, (0, 0))
        clock = pygame.time.Clock()
        clock.tick(FPS)
        for x, y in zip(enemy_x, enemy_y):
            try:
                red = pygame.Rect(x, y, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
                iscollision(player.x, player.y, red.x, red.y)
            except TypeError:
                continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(player.x + player.width // 2, player.y, 5, 10)
                    bullets.append(bullet)
                    if player.y < HEIGHT - SPACE_SHIP_HEIGHT - 6:
                        player.y += 2
        for i in range(enemies_no):
            if enemy_x[i] is not None:
                enemy_x[i] += enemy_x_change[i]
                if enemy_x[i] <= 0:
                    enemy_x_change[i] = 1
                    enemy_y[i] += enemy_y_change[i]
                if enemy_x[i] >= WIDTH - SPACE_SHIP_WIDTH:
                    enemy_x_change[i] = -1
                    enemy_y[i] += enemy_y_change[i]
                screen.blit(SPACE_SHIP_RED, (enemy_x[i], enemy_y[i]))
                screen.blit(SPACE_SHIP_YELLOW, (player.x, player.y))
        keybinding(player, bullets)
        for bullet in bullets:
            pygame.draw.rect(screen, (0, 0, 255), bullet)
            bullet.y -= 10
            if bullet.y <= 0:
                bullets.remove(bullet)
            c = 0
            for x, y, z in zip(enemy_x, enemy_y, enemy_health):
                try:
                    if enemy_x[c] is not None:
                        red = pygame.Rect(x, y, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
                        if bullet.colliderect(red):
                            # BULLET_HIT_SOUND.play()
                            if bullet in bullets:
                                bullets.remove(bullet)
                            if z != 0:
                                z -= 1
                                enemy_health[c] = z
                            else:
                                ENEMY_LIST_STAGE1[c] = (None, None)
                                enemy_x[c] = None
                                enemy_y[c] = None
                                if ENEMY_LIST_STAGE1.count((None, None)) == enemies_no:
                                    end_screen("You Win")
                                continue
                        elif bullet.y <= 0:
                            if bullet in bullets:
                                bullets.remove(bullet)
                    c += 1
                except TypeError:
                    continue
        pygame.display.update()


if __name__ == "__main__":
    main()

    # for x in range(WIDTH):
    #     for y in range(HEIGHT):
    #         if x % 100 == 0 and 50 < x < 800:
    #             if y % 100 == 0 and y < 500:
    #                 li.append((x, y))
    #                 print(li)
