import pygame
import heroes
import random
import sys
from os import path
import time
pygame.init()
size = width, height = 600,800
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("SpaceWar")
black = (0, 0, 0)
white = (255,255,255)
green = (0, 255, 0) 
blue = (0, 0, 128) 
myFont = pygame.font.SysFont("monospace", 35)
clock = pygame.time.Clock()

def allgame():
    img_dir = path.join(path.dirname(__file__), 'img')
    FPS = 60
    direction = 'up'
    gameLoop = True
    imageBC = pygame.image.load('img/backround_img.gif').convert_alpha()
    colorRED = (255, 0, 0)
    SPEED = 2
    score = 0
    health = 3
    frame_count = 0
    time = "1 0. 0"


    explosion = pygame.image.load('img/explosion0.png')

    player = heroes.Heroes(15, 5)
    player_size = 40
    hero_img = pygame.image.load('img/Myship.png')
    hero_imgRes = pygame.transform.scale(hero_img, (65, 65))
    player_pos = hero_img.get_rect(midbottom=(width/2, 700))

    shoot = pygame.image.load('img/pixil-frame-0.png')
    shoots_pos = shoot.get_rect(midbottom=(player_pos[0], 700))
    shoots_list = shoots_pos

    smallEnemyPattern = heroes.Heroes(10, 2)
    smallEnemy = pygame.image.load('img/enemy.png')
    smallEnemy_size = 65
    smallEnemy_pos = [random.randint(0,width-smallEnemy_size), 100]
    smallEnemy_list = [smallEnemy_pos]

    def draw_text(text,font,color,window, x,y):
        textobj = font.render(text,35, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        window.blit(textobj, textrect)

    def drop_enemies(smallEnemy_list):
        delay = random.random()
        if len(smallEnemy_list) < 5 and delay < 0.1:
            x_pos = random.randint(0, width-smallEnemy_size)
            y_pos = 0
            smallEnemy_list.append([x_pos, y_pos])
    
    def draw_enemies(smallEnemy_list):
        for smallEnemy_pos in smallEnemy_list:
            window.blit(smallEnemy, smallEnemy_pos)

        for idx, smallEnemy_pos in enumerate(smallEnemy_list):
            if smallEnemy_pos[1] >= 0 and smallEnemy_pos[1] < height:
                smallEnemy_pos[1] += SPEED
            else:
                smallEnemy_list.pop(idx)


    def collision_check(smallEnemy_list, shoots_pos):
        for idx, smallEnemy_pos in enumerate(smallEnemy_list):
            if detect_collision(smallEnemy_pos, shoots_pos):
                return True, smallEnemy_list.pop(idx)
                
        return False


    def detect_collision(smallEnemy_pos, shoots_pos):
        p_x = smallEnemy_pos[0]
        p_y = smallEnemy_pos[1]

        e_x = shoots_pos[0]
        e_y = shoots_pos[1]

        if (e_x >= p_x and e_x < (p_x + smallEnemy_size)) or (p_x >= e_x and p_x < e_x):
            if (e_y >= p_y and e_y < (p_y + smallEnemy_size)) or (p_y >= e_y and p_y < e_y):
                return True
        return False

    def dec_col_player(player_pos, smallEnemy_pos):
        p_x = player_pos[0]
        p_y = player_pos[1]

        e_x = smallEnemy_pos[0]
        e_y = smallEnemy_pos[1]

        if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + smallEnemy_size)):
            if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + smallEnemy_size)):
                return True
        return False


    while gameLoop:
        pygame.time.Clock().tick(60)
        frame_count += 1

        hour = int(time[0])
        minute = int(time[2])
        second = int(time[5])

        if second > 0 and frame_count == 20:
            frame_count = 0
            second -= 1
        if second == 0 and minute > 0 and frame_count == 20:
            frame_count = 0
            second = 8
            minute -= 1
        if minute == 0 and hour > 0 and frame_count == 20:
            frame_count = 0
            minute = 9
            second = 8
            hour -= 1
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                x = player_pos[0]
                x1 = shoots_pos[0]
                y = player_pos[1]
                y1 = shoots_pos[1]
                if e.key == pygame.K_LEFT or e.key == ord('a'):
                    x -= 40
                elif e.key == pygame.K_RIGHT or e.key == ord('d'):
                    x += 40
                player_pos = [x,y]

        if direction == 'down':
            shoots_pos[1] = player_pos[1]
        elif direction == 'up':
            shoots_pos.centery -= 20
        elif collision_check(smallEnemy_list, shoots_pos):
            shoots_pos[1] = player_pos[1]

        if shoots_pos.bottom > height:
            direction = 'up'
        if shoots_pos.top < 0:
            direction = 'down'
        
        if shoots_pos[1] == player_pos[1]:
            direction = 'up' 
            shoots_pos[0] = player_pos[0] + 27
    
        time = str(hour) + " " + str(minute) + ". " + str(second)
        font_time = pygame.font.SysFont('monospace', 35, False, False)
        text_time = font_time.render(time, True, green)
        drop_enemies(smallEnemy_list)

        window.blit(imageBC, [0,0])
        window.blit(shoot, shoots_pos)
        window.blit(hero_imgRes, player_pos)
        draw_enemies(smallEnemy_list)

        if collision_check(smallEnemy_list, shoots_pos):
            direction = 'down'
            score += 1
        text = "Score:" + str(score)
        
        draw_text(text, myFont, white, window, width-200, height-40)

        if second == 0 and minute == 0 and hour == 0:
            gameLoop = False
            yourScore(score)
        if dec_col_player(player_pos, smallEnemy_pos):
            health -= 1
            print(health)
        if health == 0:
            gameLoop = False
        clock.tick(FPS)
        pygame.display.update()


def button(msg, x,y, w,h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == 1 and action != None:
        if action == 'play':
            allgame()
        elif action == 'tomenu':
            main_menu()


    pygame.draw.rect(window, black, (250, 450, 100, 50))
    text_btn = msg 
    textobj_btn = myFont.render(text_btn, 35, white)
    text_btn_rect = textobj_btn.get_rect()
    text_btn_rect.center = ((x + (w/2)), (y + (h/2)))
    window.blit(textobj_btn, text_btn_rect)

def yourScore(score):
    white = (255,255,255)
    dark = (0,0,0)
    myFont = pygame.font.SysFont("monospace", 35)
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(black)
        font_f = pygame.font.SysFont("monospace", 35)
        textSurf = 'Your score: ' + str(score)
        textobj = myFont.render(textSurf, 35, white)
        textrect = textobj.get_rect()
        textrect.topleft = (180, 380)
        window.blit(textobj, textrect)

        button('Play Again', 250,425, 100,50, 'tomenu')

        pygame.display.update()
        clock.tick(5)

def main_menu():
    white = (255,255,255)
    dark = (0,0,0)
    myFont = pygame.font.SysFont("monospace", 35)
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill((209, 209, 209))
        font_f = pygame.font.SysFont("monospace", 35)
        textSurf = 'SPACEWAR'
        textobj = myFont.render(textSurf, 35, black)
        textrect = textobj.get_rect()
        textrect.topleft = (225, 400)
        window.blit(textobj, textrect)
        
        textAuthor = 'Made By Tiurin Dima'
        fontAuthor = pygame.font.SysFont("monospace", 15)
        def draw_text(text,font,color,window, x,y):
            textobj = font.render(text, 10, color)
            textrect = textobj.get_rect()
            textrect.topleft = (x,y)
            window.blit(textobj, textrect)
            
        draw_text(textAuthor, fontAuthor, dark, window ,width-200, height-40)

        button('Start', 250,450, 100,50, 'play')

        pygame.display.update()
        clock.tick(5)

main_menu()

