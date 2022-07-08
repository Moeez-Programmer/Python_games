from cryptography.fernet import Fernet
import pygame
code = b"""
pygame.init()
width = 600
height = 600
res = (width, height)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("Tic Tac Toe")
background = (255, 150, 150)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
hover_color = (255, 204, 203)
clicked_quit = False
clicked_restart = False
quit_rect = pygame.Rect(150, 200, 90, 50)
restart_rect = pygame.Rect(300,200,140,50)
btn_rect_list = [quit_rect,restart_rect]
rect_list = [
    pygame.Rect(10, 10, 180, 190),
    pygame.Rect(200, 10, 190, 190),
    pygame.Rect(400, 10, 190, 190),
    pygame.Rect(10, 210, 180, 180),
    pygame.Rect(200, 210, 190, 180),
    pygame.Rect(400, 210, 190, 180),
    pygame.Rect(10, 400, 180, 190),
    pygame.Rect(200, 400, 190, 190),
    pygame.Rect(400, 400, 190, 190)]
clicked_list = [0 for _ in rect_list]
board_list = [None for _ in rect_list]
x_turn = True
o_turn = False
win_countx = 0
win_counto = 0
draw_count = 0


def make_text(text,place,size):
    pygame.font.init()
    font = pygame.font.SysFont("Corbel", size)
    text = font.render(text, True, (0, 0, 255))
    screen.blit(text, place)


def draw_x(x, y, width, height):
    for i in range(5):
        pygame.draw.aaline(screen, "blue", (x + i, y), (
        width + x + i, height + y))  # start_pos(x+thickness,y)---end_pos(width+x+thickness,height+y)
        pygame.draw.aaline(screen, "blue", (width + x + i, y),
                           (x + i, height + y))  # start_pos(x+width+thickness,y)---end_pos(x+thickness,y+height)


def draw_line():
    line_color = (212, 212, 255)
    pygame.draw.rect(screen, line_color, (190, 10, 10, 580))
    pygame.draw.rect(screen, line_color, (390, 10, 10, 580))
    pygame.draw.rect(screen, line_color, (10, 200, 580, 10))
    pygame.draw.rect(screen, line_color, (10, 390, 580, 10))


def highlight():
    for rect in rect_list:
        if rect.collidepoint(mouse):  # rect.collidepoint((x,y)) returns true if mouse x,y pos is on rect
            pygame.draw.rect(screen, hover_color, rect)


def draw_board():
    for i, rect in enumerate(rect_list):
        if clicked_list[i] == 1:
            board_list[i] = True
            pygame.draw.rect(screen, background, rect)
            draw_x(rect.x, rect.y, rect.width, rect.height)
        if clicked_list[i] == 2:
            board_list[i] = False
            pygame.draw.rect(screen, background, rect)
            pygame.draw.ellipse(screen, "blue", rect, 5)


done = False
h = 0


def win():
    global done,win_countx,win_counto,h
    if board_list[0] == board_list[1] == board_list[2] == True\
            or board_list[3] == board_list[4] == board_list[5] == True\
            or board_list[6] == board_list[7] == board_list[8] == True\
            or board_list[0] == board_list[4] == board_list[8] == True\
            or board_list[2] == board_list[4] == board_list[6] == True\
            or board_list[0] == board_list[3] == board_list[6] == True\
            or board_list[1] == board_list[4] == board_list[7] == True\
            or board_list[2] == board_list[5] == board_list[8] == True:
        if h < 1:
            win_countx += 1
        h += 1
        menu_screen("X Wins!")
        done = True
    elif board_list[0] == board_list[1] == board_list[2] == False\
            or board_list[3] == board_list[4] == board_list[5] == False\
            or board_list[6] == board_list[7] == board_list[8] == False\
            or board_list[0] == board_list[4] == board_list[8] == False\
            or board_list[2] == board_list[4] == board_list[6] == False\
            or board_list[0] == board_list[3] == board_list[6] == False\
            or board_list[1] == board_list[4] == board_list[7] == False\
            or board_list[2] == board_list[5] == board_list[8] == False:
        if h < 1:
            win_counto += 1
        h += 1
        menu_screen("O Wins!")
        done = True


def menu_screen(text):
    win_place = (150, 50)
    screen.fill("white")
    make_text(text, win_place, 100)
    if restart_rect.collidepoint(mouse):
        pygame.draw.rect(screen, (200, 200, 200), restart_rect)
    if quit_rect.collidepoint(mouse):
        pygame.draw.rect(screen, (200, 200, 200), quit_rect)
    make_text("Quit", (150, 200), 50)
    make_text("Restart", (300, 200), 50)
    make_text("Wins:", (150,250),100)
    make_text(f"X:{win_countx}",(160,350),50)
    make_text(f"O:{win_counto}",(155,400),50)
    make_text(f"Draws:{draw_count}",(150,450),50)


draw = False


def drawf():
    global draw,h,draw_count
    if None not in board_list and not done:
        menu_screen("DRAW!!")
        draw = True
        if h < 1:
            draw_count += 1
        h += 1
    return draw


while True:
    mouse = pygame.mouse.get_pos()
    x = screen.get_at(mouse)[:3]
    screen.fill(background)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            if quit_rect.collidepoint(ev.pos) and done or quit_rect.collidepoint(ev.pos) and draw:
                clicked_quit = True
            if restart_rect.collidepoint(ev.pos) and done or restart_rect.collidepoint(ev.pos) and draw:
                clicked_restart = True
            for i, rect in enumerate(rect_list):  # enumerate returns two variable only need to feed the iteration value
                if rect.collidepoint(ev.pos) and x == hover_color:  # ev.pos returns position of mouse it is associated with MOUSEBUTTONDOWN
                    if x_turn:
                        clicked_list[i] = 1
                    elif o_turn:
                        clicked_list[i] = 2
                    x_turn = not x_turn
                    o_turn = not o_turn
            if clicked_quit:
                pygame.quit()
            if clicked_restart:
                clicked = False
                clicked_restart = False
                clicked_quit = False
                clicked_list = [0 for _ in rect_list]
                board_list = [None for _ in rect_list]
                done = False
                draw = False
                h = 0
                continue
    draw_line()
    highlight()
    draw_board()
    win()
    drawf()
    pygame.display.update()"""

key = Fernet.generate_key()

encryption_type = Fernet(key)
encrypted_message = encryption_type.encrypt(code)

decrypted_message = encryption_type.decrypt(encrypted_message)

exec(decrypted_message)
