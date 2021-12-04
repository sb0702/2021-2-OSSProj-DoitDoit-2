import pygame
import operator
import math
from random import *
from pygame.display import mode_ok
from pygame.locals import *
import pymysql
from pymysql.cursors import Cursor
from mino import *
from ui import *
from init_values import *
import time
from pygame.rect import Rect

min_width = 600
min_height = 350
board_rate = 0.5
pygame.init()
pygame.key.set_repeat(500)


tetris = pymysql.connect(
            user='admin',
            password='tjgus1234',
            host='mytetris.cw4my8jpnexs.ap-northeast-2.rds.amazonaws.com',
            db='tetris',
            charset='utf8'
        )
# 소리 크기 설정
def set_volume():
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.move_sound.set_volume(effect_volume / 10)
    ui_variables.drop_sound.set_volume(effect_volume / 10)
    ui_variables.single_sound.set_volume(effect_volume / 10)
    ui_variables.double_sound.set_volume(effect_volume / 10)
    ui_variables.triple_sound.set_volume(effect_volume / 10)
    ui_variables.tetris_sound.set_volume(effect_volume / 10)
    ui_variables.background_sound.set_volume(effect_volume / 40)
    ui_variables.item_eraseline.set_volume(effect_volume / 20)
    ui_variables.item_getuse.set_volume(effect_volume / 10)
    



# Draw block 
def draw_block(x, y, color): 
    if color == ui_variables.t_color[row_mino]:
        draw_image(screen, ui_variables.row_image, x,y, block_size, block_size ) # 아이템 블록은 이미지로, row_item
    elif color == ui_variables.t_color[col_mino]:
        draw_image(screen, ui_variables.col_image, x, y, block_size, block_size ) # 아이템 블록은 이미지로, col_item
    elif color == ui_variables.t_color[bomb_mino]:
        draw_image(screen, ui_variables.bomb_image, x,y, block_size, block_size ) # 아이템 블록은 이미지로, bomb_item
    elif color == ui_variables.t_color[itembox_mino]: 
        draw_image(screen, ui_variables.itembox_image, x,y, block_size, block_size ) # 아이템 블록은 이미지로, bomb_item
    else: # 기본 블록들은 정사각형 그리기 -> 속도 개선
        pygame.draw.rect(
            screen,
            color,
            Rect(x, y, block_size, block_size)
        )

    # 테두리 그리기 
    pygame.draw.rect( 
        screen,
        ui_variables.grey_4,
        Rect(x, y, block_size, block_size),
        1
    )

def draw_image(window, img_path, x, y, w, h):
    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (w, h))
    window.blit(image, (x, y))

# 블록을 이미지로 넣기 
def draw_block_image(x, y, image): # image에는 ui에 있는, 색깔블록~아이템 블록이 담긴 t_block이 들어감
    draw_image(screen, image, x, y, block_size, block_size) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)



# Draw game screen
def draw_board(next, hold, score, level, goal):
    screen.fill(ui_variables.grey_1)
    sidebar_width = int(SCREEN_WIDTH * 0.5312)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(SCREEN_WIDTH * 0.2375), SCREEN_HEIGHT)  #(X축, y축, 가로, 세로)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_size):
        for j in range(mino_turn):
            dx = int(SCREEN_WIDTH * 0.13) + sidebar_width + block_size * j
            dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(mino_size):
            for j in range(mino_turn):
                dx = int(SCREEN_WIDTH * 0.025) + sidebar_width + block_size * j
                dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)
    text_fever = ui_variables.h5.render("FEVER TIME", 1, ui_variables.black)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.15) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_score, text_score.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5187))))
    screen.blit(score_value, score_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5614))))
    screen.blit(text_level, text_level.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.6791))))
    screen.blit(level_value, level_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.7219))))
    screen.blit(text_goal, text_goal.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8395))))
    screen.blit(goal_value, goal_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8823))))
    #screen.blit(text_fever, text_fever.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.2780))))

    # Draw board
    # 기본 크기에 맞춰 레이아웃이 설정되어 있으므로 조정해준다.
    width_adjustment = (DEFAULT_WIDTH - width) // 2
    height_adjustment = (DEFAULT_HEIGHT - height) // 2

    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.25) + block_size * (width_adjustment + x)
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * (height_adjustment + y)
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])


# 하드모드 보드
def draw_hardboard(hold, score, level, goal):
    screen.fill(ui_variables.grey_1)
    sidebar_width = int(SCREEN_WIDTH * 0.5312)
    
    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(SCREEN_WIDTH * 0.2375), SCREEN_HEIGHT)  #(X축, y축, 가로, 세로)
    )
   
    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(mino_size):
            for j in range(mino_turn):
                dx = int(SCREEN_WIDTH * 0.16 / 2) + sidebar_width + block_size * j
                dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.21 / 2) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_score, text_score.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5187))))
    screen.blit(score_value, score_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5614))))
    screen.blit(text_level, text_level.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.6791))))
    screen.blit(level_value, level_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.7219))))
    screen.blit(text_goal, text_goal.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8395))))
    screen.blit(goal_value, goal_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8823))))

    # Draw board
    # 기본 크기에 맞춰 레이아웃이 설정되어 있으므로 조정해준다.
    width_adjustment = (DEFAULT_WIDTH - width) // 2
    height_adjustment = (DEFAULT_HEIGHT - height) // 2

    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.25) + block_size * (width_adjustment + x)
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * (height_adjustment + y)
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])


def draw_reverse_board(next, hold, score, level, goal):
    screen.fill(ui_variables.grey_1)
    sidebar_width = int(SCREEN_WIDTH * 0.5312)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(SCREEN_WIDTH * 0.2375), SCREEN_HEIGHT)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]
    
    for i in range(mino_size):
        for j in range(mino_turn):
            dx = int(SCREEN_WIDTH * 0.13) + sidebar_width + block_size * j
            dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(mino_size):
            for j in range(mino_turn):
                dx = int(SCREEN_WIDTH * 0.025) + sidebar_width + block_size * j
                dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)
    text_fever = ui_variables.h5.render("FEVER TIME", 1, ui_variables.black)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.15) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_score, text_score.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5187))))
    screen.blit(score_value, score_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5614))))
    screen.blit(text_level, text_level.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.6791))))
    screen.blit(level_value, level_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.7219))))
    screen.blit(text_goal, text_goal.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8395))))
    screen.blit(goal_value, goal_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8823))))
    screen.blit(text_fever, text_fever.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.2780))))
    


    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.25) + block_size * x
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])


def draw_1Pboard(next, hold):
    sidebar_width = int(SCREEN_WIDTH * 0.3112)  # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(SCREEN_WIDTH * 0.1875), SCREEN_HEIGHT)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  # 다음 블록의 원래 모양

    for i in range(mino_size):  # 다음 블록
        for j in range(mino_turn):
            dx = int(SCREEN_WIDTH * 0.045) + sidebar_width + block_size * j
            dy = int(SCREEN_HEIGHT * 0.3743) + block_size * i
            if grid_n[i][j] != 0:  # 해당 부분에 블록이 있으면
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )
    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(mino_size):
            for j in range(mino_turn):
                dx = int(SCREEN_WIDTH * 0.045) + sidebar_width + block_size * j
                dy = int(SCREEN_HEIGHT * 0.1336) + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_at = ui_variables.h5.render("ATTACK", 1, ui_variables.black)
    at_value = ui_variables.h4.render(str(attack_point), 1, ui_variables.black)
    text_player = ui_variables.h5.render("1Player", 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.2780)))
    screen.blit(text_score, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.5187)))
    screen.blit(score_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.5614)))
    screen.blit(text_at, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.6791)))
    screen.blit(at_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.7219)))
    screen.blit(text_player, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.8815)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.05) + block_size * x
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])


def draw_2Pboard(next, hold):
    sidebar_width = int(SCREEN_WIDTH * 0.7867)  # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(SCREEN_WIDTH * 0.1875), SCREEN_HEIGHT)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  # 다음 블록의 원래 모양

    for i in range(mino_size):  # 다음 블록
        for j in range(mino_turn):
            dx = int(SCREEN_WIDTH * 0.045) + sidebar_width + block_size * j
            dy = int(SCREEN_HEIGHT * 0.3743) + block_size * i
            if grid_n[i][j] != 0:  # 해당 부분에 블록이 있으면
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )  # 블록 이미지 출력

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino_2P != -1:
        for i in range(mino_size):
            for j in range(mino_turn):
                dx = int(SCREEN_WIDTH * 0.045) + sidebar_width + block_size * j
                dy = int(SCREEN_HEIGHT * 0.1336) + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score_2P), 1, ui_variables.black)
    text_at = ui_variables.h5.render("ATTACK", 1, ui_variables.black)
    at_value = ui_variables.h4.render(str(attack_point_2P), 1, ui_variables.black)
    text_player = ui_variables.h5.render("2Player", 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.2780)))
    screen.blit(text_score, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.5187)))
    screen.blit(score_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.5614)))
    screen.blit(text_at, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.6791)))
    screen.blit(at_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.7219)))
    screen.blit(text_player, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.8815)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.53) + block_size * x
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix_2P[x][y + 1]])


def draw_multiboard(next_1P, hold_1P, next_2P, hold_2P):
    screen.fill(ui_variables.grey_1)
    draw_1Pboard(next_1P, hold_1P)
    draw_2Pboard(next_2P, hold_2P)

def draw_itemboard(next, hold, score, level, goal, inven):
    screen.fill(ui_variables.grey_1)
    sidebar_x = int(SCREEN_WIDTH * 0.5312)
    sidebar_width = int(SCREEN_WIDTH * 0.2375)
    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_x, 0, sidebar_width, SCREEN_HEIGHT)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_size):
        for j in range(mino_turn):
            dx = int(SCREEN_WIDTH * 0.13) + sidebar_x + block_size * j
            dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
            if grid_n[i][j] != 0:
                draw_block_image(dx,dy,ui_variables.t_block[grid_n[i][j]]) # 블록 이미지 출력
            

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(mino_size):
            for j in range(mino_turn):
                dx = int(SCREEN_WIDTH * 0.025) + sidebar_x + block_size * j
                dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
                if grid_h[i][j] != 0:
                    draw_block_image(dx,dy,ui_variables.t_block[grid_h[i][j]]) # 블록 이미지 출력
       
    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.black)
    text_item =  ui_variables.h5.render("ITEM", 1, ui_variables.black)
    
    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_x, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.15) + sidebar_x, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_score, text_score.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_x, int(SCREEN_HEIGHT * 0.5187))))
    screen.blit(score_value, score_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_x, int(SCREEN_HEIGHT * 0.5614))))
    screen.blit(text_level, text_level.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_x, int(SCREEN_HEIGHT * 0.6791))))
    screen.blit(level_value, level_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_x, int(SCREEN_HEIGHT * 0.7219))))
    screen.blit(text_goal, text_goal.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_x, int(SCREEN_HEIGHT * 0.8395))))
    screen.blit(goal_value, goal_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_x, int(SCREEN_HEIGHT * 0.8823))))
    screen.blit(text_item, text_item.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_x, int(SCREEN_HEIGHT * 0.2780))))

    dx_inven1 = int(sidebar_x + sidebar_width * 0.25 - inven_size / 2)
    dx_inven2 = int(sidebar_x + sidebar_width * 0.5 - inven_size / 2)
    dx_inven3 = int(sidebar_x + sidebar_width * 0.75 - inven_size / 2)
    dy_inven = int(SCREEN_HEIGHT * 0.3983) - inven_size / 2
    dx_inven = [dx_inven1, dx_inven2, dx_inven3]
    
    if len(inven) > 0:
        for i in range(len(inven)):
            item = inven[i]
            item = pygame.transform.scale(item, (inven_size, inven_size))
            screen.blit(item, (dx_inven[i], dy_inven))
    else:
        pygame.draw.rect(screen,ui_variables.black, (dx_inven1, dy_inven, inven_size, inven_size),1)
        pygame.draw.rect(screen,ui_variables.black, (dx_inven2, dy_inven, inven_size, inven_size),1)
        pygame.draw.rect(screen,ui_variables.black, (dx_inven3, dy_inven, inven_size, inven_size),1)
    


    # Draw board
    # 기본 크기에 맞춰 레이아웃이 설정되어 있으므로 조정해준다.
    width_adjustment = (DEFAULT_WIDTH - width) // 2
    height_adjustment = (DEFAULT_HEIGHT - height) // 2

    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.25) + block_size * (width_adjustment + x)
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * (height_adjustment + y)
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]]) 

# Draw a tetrimino
def draw_mino(x, y, mino, r): # 블록 위치 x,y 블록 모양, 블록 방향
    grid = tetrimino.mino_map[mino - 1][r]  # 현재 블록
    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r): #테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
        ty += 1 # 한 칸 밑으로 하강

    # Draw ghost 현재 블록이 쌓일 위치 보여줌
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0: # 비어있지 않으면
                matrix[tx + j][ty + i] = 8 # ghost 블록 그려줌

    # Draw mino
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j] # matrix에 현재 블록 넣어줌





def draw_mino_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]  # grid에 mino_map의 모양과 방향을 선택한 리스트를 넣는다.
    tx, ty = x, y
    while not is_bottom_2P(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix_2P[tx + j][ty + i] = 8

    # Draw mino
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix_2P[x + j][y + i] = grid[i][j]


# Erase a tetrimino

def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]
           
    
    for j in range(height + 1):
        for i in range(width):
            if matrix[i][j] == 8:
                matrix[i][j] = 0 # ghost 블록 없애기

    # Erase mino
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0 # 블록 없애기

    # 추가적인 블록 생성해서 사용하는 아이템 쓸 때
    if item == True:
        erase_row() # 가로줄 삭제 아이템의 효과
        erase_col() # 세로줄 삭제 아이템의 효과
        bomb() # 3x3 블록 삭제 아이템의 효과
         
    


def erase_mino_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(height + 1):
        for i in range(width):
            if matrix_2P[i][j] == 8:
                matrix_2P[i][j] = 0

    # Erase mino
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix_2P[x + j][y + i] = 0


# Returns true if mino is at bottom
def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (y + i + 1) > height:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False


def is_bottom_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (y + i + 1) > height:
                    return True
                elif matrix_2P[x + j][y + i + 1] != 0 and matrix_2P[x + j][y + i + 1] != 8:
                    return True

    return False


# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False


def is_leftedge_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix_2P[x + j - 1][y + i] != 0:
                    return True

    return False


# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (x + j + 1) > width - 1:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False


def is_rightedge_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (x + j + 1) > width - 1:
                    return True
                elif matrix_2P[x + j + 1][y + i] != 0:
                    return True

    return False


# Returns true if turning right is possible
def is_turnable_r(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(mino_size):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > width - 1 or (y + i) < 0 or (y + i) > height:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True


def is_turnable_r_2P(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > width - 1 or (y + i) < 0 or (y + i) > height:
                    return False
                elif matrix_2P[x + j][y + i] != 0:
                    return False

    return True


# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > width - 1 or (y + i) < 0 or (y + i) > height:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True


def is_turnable_l_2P(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > width - 1 or (y + i) < 0 or (y + i) > height:
                    return False
                elif matrix_2P[x + j][y + i] != 0:
                    return False

    return True


# Returns true if new block is drawable
def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(mino_size):
        for j in range(mino_turn):
            # print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True


def is_stackable_2P(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(mino_size):
        for j in range(mino_turn):
            # print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix_2P[3 + j][i] != 0:
                return False

    return True

def isthereID(ID, table):
    curs = tetris.cursor()
    sql = "SELECT * FROM {} WHERE id=%s".format(table)
    curs.execute(sql, ID)
    data = curs.fetchone()
    curs.close()
    if data:
        return False
    else:
        return True
def istheresaved(name2,SavedPass,table):
    if isthereID(name2,table):
        cursor = tetris.cursor()
        sql = "INSERT INTO {} (id, password,score) VALUES (%s,%s,%s)".format(table)
        cursor.execute(sql, (name2, SavedPass,score))
        tetris.commit()  
        cursor.close() ## tetris db insert 
    else :      
        cursor = tetris.cursor()
        sql = "select score from {} where id =%s".format(table)
        cursor.execute(sql, SavedID)   ## 명섭
        result = cursor.fetchone()
        if result[0] < score:                           
            sql = "Update {} set score = %s where id =%s".format(table)
            cursor.execute(sql, (score,name2))
            tetris.commit()  
            cursor.close() ## tetris db insert 
        else: pass
def LoginPass(ID, table, password):
    curs = tetris.cursor()
    sql = "SELECT * FROM {} WHERE id=%s and password = %s".format(table)
    curs.execute(sql, (ID,password))
    Findedpassword = curs.fetchone()
    if Findedpassword:
        return True
    else:
        return False
  
def LoginID(table, ID):
    curs = tetris.cursor()
    sql = "SELECT password FROM {} WHERE id=%s".format(table)
    curs.execute(sql, ID)
    data = curs.fetchone()
    curs.close()
    if data:
        return True
    else:
        return False

def LoginCom(ID,table,password):   
    if LoginID(table,ID):
        if LoginPass(ID, table, password): 
            ## 명섭
            print("정답")
            return True
        else:
            print("암호 틀림")
            return False             
    else:
        print("신규")
        return False
        
        

def DrawBar(pos, size, borderC, barC, progress):
    
    pygame.draw.rect(screen, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+3, pos[1]+3)
    innerSize = ((size[0]-6) * progress, size[1]-6)
    pygame.draw.rect(screen, barC, (*innerPos, *innerSize))


# 아이템 획득~인벤토리 관련 함수 
def get_item():
    if len(inven)<3:
        inven.append(item_list[randrange(0,5)]) # 랜덤으로 얻음

def use_item(key): # 사용자의 키조작 전달 받기
    if len(inven)>0:
        item_u = inven[key-1] # 인벤토리의 key번째 칸 아이템
        inven.pop(key-1) # 사용한 아이템은 삭제
    return item_u


# 아이템 사용 함수
def earthquake(): # 맨 아래 줄 삭제 아이템
    cnt_box=0
    for i in range(width): # 가로줄 전체에 대해서
        if matrix[i][height] == itembox_mino:
            cnt_box +=1
        matrix[i][height] = 0 
    while cnt_box > 0: # 깬 박스 수만큼
        get_item()
        ui_variables.item_getuse.play() 
        cnt_box -=1  
    k = height
    while k > 0:  # 남아있는 블록 아래로 한 줄씩 내리기
        for i in range(width):
            matrix[i][k] = matrix[i][k-1]
        k -= 1       

def board_reset():
    for j in range(height+1):
        for i in range(width):
            matrix[i][j] = 0 # 보드 내 블록 다 비워버리기

def erase_row():    # 가로줄 삭제 아이템 효과
    cnt_box = 0
    for j in range(height+1):
        for i in range(width):
            if matrix[i][j] == row_mino: # i_row 블록이면
                k = j # y 좌표 기억
                if matrix[i][k] == itembox_mino:
                    cnt_box +=1
                matrix[i][k] = 0 # 해당 줄 삭제
                while k>0: 
                    for i in range(width):
                        matrix[i][k] = matrix[i][k-1] # 지워진 줄 위에 있던 블록 한 줄씩 내리기
                    k -= 1
    while cnt_box > 0: # 깬 박스 수만큼
        get_item()
        ui_variables.item_getuse.play() 
        cnt_box -=1 

def erase_col(): # 세로줄 삭제 아이템 효과
    cnt_box = 0
    for i in range(width):
        for j in range(height+1):
            if matrix[i][j] == col_mino: # i_col 블록이면
                k = i # x 좌표 기억
                if matrix[k][j] == itembox_mino:
                    cnt_box +=1
                y = height
                while y>0:
                    matrix[k][y] = 0 # i_col 블록이 위치한 세로줄 삭제
                    y -= 1
    while cnt_box > 0: # 깬 박스 수만큼
        get_item()
        ui_variables.item_getuse.play() 
        cnt_box -=1 
    
def bomb():# 3x3 블록 삭제 아이템 효과
    cnt_box=0
    for j in range(height+1):
        for i in range(width):
            if matrix[i][j] == bomb_mino: # i_bomb 블록이면
                m = i-1 # 3x3 블록 없애주니까 i-1 ~ i+1 번째 지위져야 함
                n = j -1
                for k in range(bomb_size): # 3x3이므로
                    for q in range(bomb_size): # 
                        if m+k >= 0 and m+k<width and n+q >= 0 and n+q<=height: # 블록이 있든 없든
                            if matrix[m+k][n+q] == itembox_mino:
                                cnt_box += 1
                            matrix[m+k][n+q] = 0 # 3x3만큼 다 지워줌
    while cnt_box > 0: # 깬 박스 수만큼
        get_item()
        ui_variables.item_getuse.play() 
        cnt_box -=1 



# Start game
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 7)
pygame.display.set_caption("TTOTRIS™")
set_volume()

            
SavedID = ""
text = "ID"
password = "PASSWORD"
SavedPass = ""
text_surf = ui_variables.h2_i.render(text, True, (0, 0, 0)) 
pass_surf = ui_variables.h2_i.render(password, True, (0, 0, 0)) 
color = ui_variables.color_inactive

# 초기화 부분을 하나로 합쳐준다.
def init_game(board_width, board_height, mode, game_difficulty):
    global width, height, matrix, matrix_2P, difficulty, framerate, mode_selected, comboCounter
    comboCounter =0
    width = board_width
    height = board_height

    matrix = [[0 for y in range(board_height + 1)] for x in range(board_width)]
    matrix_2P = [[0 for y in range(board_height + 1)] for x in range(board_width)]

    mode_selected = mode
    difficulty = game_difficulty
    framerate -= math.ceil(difficulty * speed_change)


###########################################################
# Loop Start
###########################################################
## timer start

while not done:
    # Pause screen
    if pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                if reverse:
                    draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                elif pvp:
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)
                elif item: # 아이템 보드 추가
                    draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                elif hard: # 하드모드 보드 추가
                    draw_hardboard(hold_mino, score, level, goal)
                else:
                    draw_board(next_mino1, hold_mino, score, level, goal)

                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.white)
                pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.white)
                back_main = ui_variables.h5.render("Press Enter to main page", 1, ui_variables.white)

                screen.blit(pause_text, (SCREEN_WIDTH * 0.0367, SCREEN_HEIGHT * 0.1667))
                screen.blit(pause_start, (SCREEN_WIDTH * 0.033, SCREEN_HEIGHT * 0.2667))
                screen.blit(back_main, (SCREEN_WIDTH * 0.033, SCREEN_HEIGHT * 0.3333))
                pygame.display.update()

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                elif event.key == K_RETURN:
                    
                    start = False
                    pause = False
                    
                    page, selected = MENU_PAGE, 0
                    set_difficulty = 0
                    width = DEFAULT_WIDTH
                    height = DEFAULT_HEIGHT
                    ui_variables.click_sound.play()
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    next_mino2 = randint(1, 7)
                    hold_mino = -1
                    item_mino = randint(1, 9)

                    framerate = 30
                    fever_score = 500
                    hard_score = 500
                    next_fever = 500
                    max_score = 99999
                    fever_interval = 3
                    interval = 3
                    score = 0
                    fever = 0
                    level = 1
                    goal = level * 2
                    bottom_count = 0
                    hard_drop = False
                    inven = [] # 인벤토리 리셋
                    hard_i = 1
                    #hard = False

                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    min_width = 700
                    min_height = 350
                    board_rate = 0.5

                    hold_2P = False
                    dx_2P, dy_2P = 3, 0
                    rotation_2P = 0
                    mino_2P = randint(1, 7)
                    next_mino_2P = randint(1, 7)
                    hold_mino_2P = -1
                    bottom_count_2P = 0
                    hard_drop_2P = False
                    attack_point = 0
                    attack_point_2P = 0
                    score_2P = 0
                    level_2P = 1
                    goal_2P = level_2P * 2
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]
                    player = 0
                    attack_stack = 0
                    attack_stack_2P = 0
                    erase_stack = 0
                    erase_stack_2P = 0

                    if pvp:
                        pvp = False

                    if reverse:
                        reverse = False

                    if item:
                        item = False


            elif event.type == VIDEORESIZE:
                
                SCREEN_WIDTH = event.w

                SCREEN_HEIGHT = event.h

                if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                    SCREEN_WIDTH = min_width

                    SCREEN_HEIGHT = min_height

                if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                    board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                    SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                    SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌
                
                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                
    # Game screen
    elif start:        
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            # 여기서 부터 겜 스타트
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, framerate * 6) 
                # Draw a mino

                draw_mino(dx, dy, mino, rotation)
                
                if reverse:
                    draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                elif item: # 아이템 보드 추가
                    draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                elif hard: # 하드모드 보드 추가
                    draw_hardboard(hold_mino, score, level, goal)
                else:
                    draw_board(next_mino1, hold_mino, score, level, goal)
                    
                pygame.display.update()

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down 떨구는 함수
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1 # 떨어지는 변화량
                
                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        if reverse:
                            draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                        elif item: # 아이템 보드 추가
                            draw_itemboard(next_mino1, hold_mino, score, level, goal, inven) 
                        elif hard: # 하드모드 보드 추가
                            draw_hardboard(hold_mino, score, level, goal)                        
                        else:
                            draw_board(next_mino1, hold_mino, score, level, goal)
                        if is_stackable(next_mino1):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            if item:
                                next_mino2 = randint(1, 9)
                            else:
                                next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_over = True
                            if reverse:
                                reverse = False
                                reverse_over = True
                            if item:
                                item = False
                                item_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1
                
                # Erase line
                erase_count = 0
                for j in range(q, height+1):   
                    is_full = True
                    for i in range(width): 
                        if matrix[i][j] == 0:
                            is_full = False
                        if matrix[i][j] == 9: # 맨 밑줄 꽉 차있는데 하드모드이면
                            if hard:
                                is_full = False # 꽉 차지 않은 걸로 인식 -> 방해블록 안 깨짐
                        
                    if is_full:
                        erase_count += 1
                        comboCounter += 1
                        k = j
                        cnt_box =0 # 한 줄에 아이템 박스 몇 개 깨졌는지
                        for i in range(width):
                            if matrix[i][j] == itembox_mino: # 아이템 박스 블록 깨면
                                cnt_box +=1
                        while cnt_box > 0: # 깬 박스 수만큼
                            get_item()
                            ui_variables.item_getuse.play() 
                            cnt_box -=1  
                        while k > 0:
                            for i in range(width):
                                matrix[i][k] = matrix[i][k-1]
                            k -= 1
                    

                # 점수 계산
                # 콤보 효과?
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 100 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 200 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 500 * level
                
                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    # 하드모드 레벨업 시 방해블록 생성
                    if hard:
                        level += 1
                        # 레벨업시 이미지 출력
                        screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                        (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                    (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))
                        pygame.display.update()
                        pygame.time.delay(100)
                        goal += level * 2
                        framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                        pygame.time.set_timer(pygame.USEREVENT, framerate)
                        # 기존 있던 블럭들 한 칸씩 증가                        
                        for j in range(height):
                            for i in range(width):
                                matrix[i][j] = matrix[i][j + 1]
                        
                        for i in range(width):                            
                            matrix[i][height] = 9 # 꽉 찬 방해블록 생성
                            

                    else:
                        level += 1
                        # 레벨업시 이미지 출력
                        screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                        (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                    (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))
                        pygame.display.update()
                        pygame.time.delay(100)
                        goal += level * 2
                        framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                        pygame.time.set_timer(pygame.USEREVENT, framerate)
                        # 기존 있던 블럭들 한 칸씩 증가                        
                        for j in range(height):
                            for i in range(width):
                                matrix[i][j] = matrix[i][j + 1]
                        # 방해블록이 맨밑줄을 채움 # 회색블록 = 9 ,  한 군데가 구멍나있게 증가
                        for i in range(width):
                            matrix[i][height] = 9
                        k = randint(1, 9) # 밑바닥에 비어있는 곳을 랜덤화
                        matrix[k][height] = 0 # 0은 빈칸
                        

                # 콤보횟수에 따른 피버타임

                if feverTimeAddScore[1] > score >=feverTimeAddScore[0]:
                    TimeDecreasedByScore = feverAddingTime[0]
                if feverTimeAddScore[2] > score >= feverTimeAddScore[1]:
                    TimeDecreasedByScore = feverAddingTime[1]
                if  feverTimeAddScore[3] > score >= feverTimeAddScore[2]:
                    TimeDecreasedByScore = feverAddingTime[2]
                if  feverTimeAddScore[4] > score >= feverTimeAddScore[3]:
                    TimeDecreasedByScore = feverAddingTime[3]
                if  score >= feverTimeAddScore[4]:
                    TimeDecreasedByScore = feverAddingTime[4]     
                if comboCounter > feverBlockGoal and mode_selected != 1 and mode_selected != 3 :
                    if fever == False:
                        t0 = time.time()
                        fever = True
                    else:
                        t1 = time.time()
                        dt = t1 -t0                                 
                        DrawBar((int(SCREEN_WIDTH*0.55), int(SCREEN_HEIGHT*0.34)),(int(SCREEN_WIDTH * 0.2), int(SCREEN_HEIGHT*0.03)),borderColor,barColor, (Basictimer-TimeDecreasedByScore - dt)/ 
                        (Basictimer-TimeDecreasedByScore))                 
                        mino = randint(1, 1)
                        next_mino1 = randint(1, 1)
                        next_fever = (c + fever_interval) * fever_score # 피버모드 점수 표시                                
                        if dt >= (Basictimer -TimeDecreasedByScore):
                            comboCounter =0
                            mino = next_mino1
                            next_mino1 = randint(1, 7)                       
                            fever = False
                
                
                # 하드모드에서 500~750, 2000~2250, 3500~3750,, 단위로 장애물 등장
                if mode_selected == 1:
                    for i in range(1, max_score, interval):
                        if score > i * hard_score and score < (i + 0.5) * hard_score: 
                            
                            barrier = pygame.transform.scale(ui_variables.hard_barrier, (int(barrier_size), int(barrier_size*0.5)))
                            dx_barrier = barrier_size * 0.35 # 장애물 x축
                            dy_barrier1 = barrier_size * 0.001 # 장애물1 y축
                            dy_barrier2 = barrier_size * 0.5 # 장애물2 y축
                            if blink1:
                                screen.blit(barrier,(dx_barrier, dy_barrier1))
                                blink1 = False
                            else:
                                blink1 = True
                            
                            if blink2:
                                screen.blit(barrier,(dx_barrier, dy_barrier2))
                                blink2 = False
                            else:
                                blink2 = True
                

                
                        
                        
                    
                    

##########키조작 부분   

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    pygame.key.set_repeat(0)
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True 
                    draw_mino(dx, dy, mino, rotation)
                    if reverse:
                        draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                    elif hard: # 하드모드 보드 추가
                        draw_hardboard(hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT:
                    pygame.key.set_repeat(0)
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1: 
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            if item:
                                next_mino2 = randint(1, 9)
                            else: 
                                next_mino2 = randint(1, 7)

                        else: # hold가 있는 상태
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    if reverse:
                        draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                    elif hard: # 하드모드 보드 추가
                        draw_hardboard(hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP:
                    pygame.key.set_repeat(0)
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    if reverse:
                        draw_reverse_board(next_mino1, hold_mino, score, level, goal)                    
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                    elif hard: # 하드모드 보드 추가
                        draw_hardboard(hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_LCTRL:
                    pygame.key.set_repeat(0)
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    if reverse:
                        draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                    elif hard: # 하드모드 보드 추가
                        draw_hardboard(hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, hold_mino, score, level, goal)

                # 왼쪽 이동, 리버스모드에선 방향키 반대
                elif event.key == K_LEFT:
                    pygame.key.set_repeat(50)
                    if reverse:
                        if not is_rightedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx += 1
                        draw_mino(dx, dy, mino, rotation)
                        draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                    else:
                        if not is_leftedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx -= 1
                        draw_mino(dx, dy, mino, rotation)
                        if item: # 아이템 보드 추가
                            draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                        elif hard: # 하드모드 보드 추가
                            draw_hardboard(hold_mino, score, level, goal)
                        else:
                            draw_board(next_mino1, hold_mino, score, level, goal)

                # 오른쪽 이동, 리버스모드에선 방향키 반대
                elif event.key == K_RIGHT:
                    pygame.key.set_repeat(50)
                    if reverse:
                        if not is_leftedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx -= 1
                        draw_mino(dx, dy, mino, rotation)
                        draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                    else:
                        if not is_rightedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx += 1
                        draw_mino(dx, dy, mino, rotation)
                        if item: # 아이템 보드 추가
                            draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                        elif hard: # 하드모드 보드 추가
                            draw_hardboard(hold_mino, score, level, goal)
                        else:
                            draw_board(next_mino1, hold_mino, score, level, goal)

                            

                # soft drop
                elif event.key == K_DOWN: 
                    if not is_bottom(dx, dy, mino, rotation):
                        dy +=1 
                    #pygame.time.set_timer(pygame.USEREVENT, values.framerate*1)
                    draw_mino(dx,dy,mino, rotation)
                    if reverse:
                        draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                    elif hard: # 하드모드 보드 추가
                        draw_hardboard(hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, hold_mino, score, level, goal)
                    #pygame.display.update()

                elif event.key == K_z: # 인벤토리 첫 번째 아이템 사용
                    
                    key = 1                    
                    if item:
                        if len(inven) != 0:
                            item_u = use_item(key) # 인벤의 아이템 반환
                            if item_u == row_inven:
                                mino = row_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                            elif item_u == col_inven:
                                mino = col_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                            elif item_u == bomb_inven:
                                mino = bomb_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                            elif item_u == reset_inven:
                                erase_mino(dx, dy, mino, rotation)
                                board_reset()
                                ui_variables.item_eraseline.play() 
                            elif item_u == earthquake_inven:
                                erase_mino(dx, dy, mino, rotation)
                                earthquake()
                                ui_variables.item_eraseline.play() 
                        draw_mino(dx, dy, mino, rotation)
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)   

                elif event.key == K_x: # 인벤토리 첫 번째 아이템 사용
                    
                    key = 2
                    if item:
                        if len(inven) > 1:
                            item_u = use_item(key) # 인벤의 아이템 반환
                            if item_u == row_inven:
                                mino = row_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                                score += 50 # 한 줄 삭제했을 때의 점수
                            elif item_u == col_inven:
                                mino = col_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                            elif item_u == bomb_inven:
                                mino = bomb_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                            elif item_u == reset_inven: # 리셋 이상함
                                erase_mino(dx, dy, mino, rotation)
                                board_reset()
                                ui_variables.item_eraseline.play() 
                            elif item_u == earthquake_inven:
                                erase_mino(dx, dy, mino, rotation)
                                earthquake()
                                ui_variables.item_eraseline.play() 
                                score += 50 # 한 줄 삭제했을 때의 점수
                        
                        draw_mino(dx,dy, mino, rotation)
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)   

                elif event.key == K_c: # 인벤토리 첫 번째 아이템 사용
                    
                    key = 3
                    if item:
                        if len(inven) >2:
                            item_u = use_item(key) # 인벤의 아이템 반환
                            if item_u == row_inven:
                                mino = row_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                                score += 50 # 한 줄 삭제했을 때의 점수
                            elif item_u == col_inven:
                                mino = col_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                            elif item_u == bomb_inven:
                                mino = bomb_mino
                                erase_mino(dx, dy, mino, rotation)
                                ui_variables.item_getuse.play() 
                            elif item_u == reset_inven:
                                erase_mino(dx, dy, mino, rotation)
                                board_reset()
                                ui_variables.item_eraseline.play() 
                            elif item_u == earthquake_inven:
                                erase_mino(dx, dy, mino, rotation)
                                earthquake()
                                ui_variables.item_eraseline.play() 
                                score += 50 # 한 줄 삭제했을 때의 점수
                        
                        draw_mino(dx,dy, mino, rotation)
                        draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)   

               
            elif event.type == KEYUP:
                pygame.key.set_repeat(300)


            elif event.type == VIDEORESIZE:
                pause = True
                SCREEN_WIDTH = event.w

                SCREEN_HEIGHT = event.h

                if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                    SCREEN_WIDTH = min_width

                    SCREEN_HEIGHT = min_height

                if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                        board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                    SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                    SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌
                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                
        pygame.display.update()





         
#### pvp 모드 
    elif pvp:
        pygame.key.set_repeat(0)  # 키반복 비활성화
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not pvp_over:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 6) 

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)
                pygame.display.update()

                # Erase a mino
                if not pvp_over:
                    erase_mino(dx, dy, mino, rotation)
                    erase_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        draw_mino(dx, dy, mino, rotation)

                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                            score += 10 * level
                        else:
                            # ui_variables.GameOver_sound.play()
                            pvp = False
                            pvp_over = True
                            player = 2
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                if not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                    dy_2P += 1

                else:
                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                        if is_stackable_2P(next_mino_2P):
                            mino_2P = next_mino_2P
                            next_mino_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                            score_2P += 10 * level_2P
                        else:
                            # ui_variables.GameOver_sound.play()
                            pvp = False
                            pvp_over = True
                            player = 1
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count_2P += 1

                # Erase line
                erase_count = 0
                erase_count_2P = 0

                for j in range(height + 1):
                    is_full = True
                    for i in range(width):
                        if matrix[i][j] == 0 or matrix[i][j] == 9: # j는 바닥부터의 높이, i는 폭
                            is_full = False
                    if is_full:
                        erase_count += 1
                        attack_stack += 1
                        erase_stack += 1
                        k = j
                        while k > 0:
                            for i in range(width):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1

                for j in range(height + 1):
                    is_full = True
                    for i in range(width):
                        if matrix_2P[i][j] == 0 or matrix_2P[i][j] == 9:
                            is_full = False
                    if is_full:
                        erase_count_2P += 1
                        attack_stack_2P += 1
                        erase_stack_2P += 1
                        k = j
                        while k > 0:
                            for i in range(width):
                                matrix_2P[i][k] = matrix_2P[i][k - 1]
                            k -= 1

                # 공격 - 한 플레이어가 두줄 지우면 상대방에게 1줄 방해블록 생성
                if attack_stack >= 2:
                    attack_stack -= 2
                    for j in range(height):
                        for i in range(width):
                            matrix_2P[i][j] = matrix_2P[i][j + 1]
                    for i in range(width):
                        matrix_2P[i][height] = 9
                    k = randint(1, 9)
                    matrix_2P[k][height] = 0
                    attack_point += 1

                if attack_stack_2P >= 2:
                    attack_stack_2P -= 2
                    for j in range(height):
                        for i in range(width):
                            matrix[i][j] = matrix[i][j + 1]
                    for i in range(width):
                        matrix[i][height] = 9
                    k = randint(1, 9)
                    matrix[k][height] = 0
                    attack_point_2P += 1

                # 1P
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 100 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 200 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 500 * level

                # 2P
                if erase_count_2P == 1:
                    ui_variables.single_sound.play()
                    score_2P += 50 * level_2P
                elif erase_count_2P == 2:
                    ui_variables.double_sound.play()
                    score_2P += 100 * level_2P
                elif erase_count_2P == 3:
                    ui_variables.triple_sound.play()
                    score_2P += 200 * level_2P
                elif erase_count_2P == 4:
                    ui_variables.tetris_sound.play()
                    score_2P += 500 * level_2P

                # Increase level
                goal -= erase_count
                goal_2P -= erase_count_2P
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 2

                if goal_2P < 1 and level_2P < 15:
                    level_2P += 1
                    goal_2P += level_2P * 2

                attack_interval = fever_interval  # attack_interval = 3
                attack_score = fever_score  # attack_score = 500

                # 1P
                for i in range(2, max_score, attack_interval):
                    if score > i * attack_score and score < (i * attack_score + 300):  # 1000~1300,2500~2800,4000~4300
                        if blink:
                            screen.blit(pygame.transform.scale(ui_variables.pvp_annoying_image,
                                                               (int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.9))),
                                        (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0))  # 이미지 깜빡거리게
                            blink = False
                        else:
                            blink = True
                # 2P
                for j in range(2, 99, attack_interval):
                    if score_2P > j * attack_score and score_2P < (
                            j * attack_score + 300):  # 1000~1300,2500~2800,4000~4300
                        if blink:
                            screen.blit(pygame.transform.scale(ui_variables.pvp_annoying_image,
                                                               (int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.9))),
                                        (SCREEN_WIDTH * 0, SCREEN_HEIGHT * 0))  # 이미지 깜빡거리게
                            blink = False
                        else:
                            blink = True

                # Increase difficulty
                if erase_stack >= 3 and erase_stack_2P >= 3:
                    erase_stack = 0
                    erase_stack_2P = 0
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(200)
                    framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                elif erase_stack > erase_stack_2P and erase_stack >= 3:
                    erase_stack = 0
                    erase_stack_2P = 0
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(200)
                    framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                elif erase_stack < erase_stack_2P and erase_stack_2P >= 3:
                    erase_stack = 0
                    erase_stack_2P = 0
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(200)
                    framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                    pygame.time.set_timer(pygame.USEREVENT, framerate)


            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                erase_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_e:  # 1P#
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    #pygame.time.set_timer(pygame.USEREVENT, 2)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                elif event.key == K_SPACE:  # 2P#
                    ui_variables.drop_sound.play()
                    while not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    #pygame.time.set_timer(pygame.USEREVENT, 2)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                # Hold
                elif event.key == K_LSHIFT:  # 1P#
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                elif event.key == K_RSHIFT:  # 2P#
                    if hold_2P == False:
                        ui_variables.move_sound.play()
                        if hold_mino_2P == -1:
                            hold_mino_2P = mino_2P
                            mino_2P = next_mino_2P
                            next_mino_2P = randint(1, 7)
                        else:
                            hold_mino_2P, mino_2P = mino_2P, hold_mino_2P
                        dx_2P, dy_2P = 3, 0
                        rotation_2P = 0
                        hold_2P = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                # Turn right
                elif event.key == K_w:  # 1P#
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                elif event.key == K_UP:  # 2P#
                    if is_turnable_r_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        rotation_2P += 1
                    # Kick
                    elif is_turnable_r_2P(dx_2P, dy_2P - 1, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P + 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P - 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P, dy_2P - 2, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P + 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P - 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P += 1
                    if rotation_2P == 4:
                        rotation_2P = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                # Turn left
                elif event.key == K_q:  # 1P#
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                elif event.key == K_m:  # 2P#
                    if is_turnable_l_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        rotation_2P -= 1
                    # Kick
                    elif is_turnable_l_2P(dx_2P, dy_2P - 1, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l_2P(dx_2P + 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P -= 1
                    elif is_turnable_l_2P(dx_2P - 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l_2P(dx_2P, dy_2P - 2, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P -= 1
                    elif is_turnable_l_2P(dx_2P + 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P -= 1
                    elif is_turnable_l_2P(dx_2P - 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P -= 1
                    if rotation_2P == -1:
                        rotation_2P = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                # Move left
                elif event.key == K_a:  # 1P#
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                elif event.key == K_LEFT:  # 2P#
                    if not is_leftedge_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                # Move right
                elif event.key == K_d:  # 1P#
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                elif event.key == K_RIGHT:  # 2P#
                    if not is_rightedge_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                # soft drop
                elif event.key == K_s:
                    if not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    #pygame.time.set_timer(pygame.USEREVENT, values.framerate*1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)
                    #pygame.display.update()
                elif event.key == K_DOWN:
                    if not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        dy_2P += 1
                    #pygame.time.set_timer(pygame.USEREVENT, values.framerate*1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)
                    #pygame.display.update()
                    

            elif event.type == VIDEORESIZE:
                pause = True
                SCREEN_WIDTH = event.w

                SCREEN_HEIGHT = event.h

                if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                    SCREEN_WIDTH = min_width

                    SCREEN_HEIGHT = min_height

                if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                    SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                    SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌
                
                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2_b.render("GAME", 1, ui_variables.white)
                over_text_2 = ui_variables.h2_b.render("OVER", 1, ui_variables.white)
                #over_start = ui_variables.h5.render("Press Enter to main page", 1, ui_variables.white)
                over_text_3 = ui_variables.h5_i.render("Press Enter to main page", 1, ui_variables.white)
                
                
                if reverse_over:
                    comboCounter = 0
                    draw_reverse_board(next_mino1, hold_mino, score, level, goal)
                elif item: # 아이템 보드 추가
                    draw_itemboard(next_mino1, hold_mino, score, level, goal, inven)
                elif hard: # 하드모드 보드 추가
                    draw_hardboard(hold_mino, score, level, goal)
                else:
                    comboCounter = 0
                    draw_board(next_mino1, hold_mino, score, level, goal)
                
                screen.blit(over_text_1, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.167))
                screen.blit(over_text_2, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.233))
                screen.blit(over_text_3, (SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.4333))
                pygame.display.update()
            
            # 마우스로 창크기조절
            elif event.type == VIDEORESIZE:
                
                SCREEN_WIDTH = event.w

                SCREEN_HEIGHT = event.h

                if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                    SCREEN_WIDTH = min_width

                    SCREEN_HEIGHT = min_height

                if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                        board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                    SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                    SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                pygame.display.update()
                
            elif event.type == KEYDOWN:        

                if event.key == K_RETURN: 
                    
                    ui_variables.click_sound.play()
                    page, selected = MENU_PAGE, 0                
                    ## 여기서부터 기록 저장
                    istheresaved(text,SavedPass,"PLAYER")            
                    if DIFFICULTY_NAMES[current_selected] == "NORMAL": ## normal  명섭
                        istheresaved(text,SavedPass,DIFFICULTY_NAMES[mode_selected])
                    if DIFFICULTY_NAMES[current_selected] == "ITEM": ## normal
                        istheresaved(text,SavedPass,DIFFICULTY_NAMES[mode_selected])
                    if DIFFICULTY_NAMES[current_selected] == "HARD": ## normal 
                        istheresaved(text,SavedPass,DIFFICULTY_NAMES[mode_selected])
                    if DIFFICULTY_NAMES[current_selected] == "REVERSE": ## normal   명섭
                        istheresaved(text,SavedPass,DIFFICULTY_NAMES[mode_selected])
                    
                    width = DEFAULT_WIDTH  # Board width
                    height = DEFAULT_HEIGHT
                    game_over = False
                    reverse_over = False
                    item_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    next_mino2 = randint(1, 7)
                    hold_mino = -1
                    item_mino = randint(1, 9)
                    inven = []
                    framerate = 30
                    fever_score = 500
                    score = 0
                    max_score = 99999
                    next_fever = 500
                    fever_interval = 3
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    min_width = 700
                    min_height = 350
                    board_rate = 0.5
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]
                    set_difficulty = 0
                    
                    # PvP모드
                    hold_2P = False
                    dx_2P, dy_2P = 3, 0
                    rotation_2P = 0
                    mino_2P = randint(1, 7)
                    next_mino_2P = randint(1, 7)
                    hold_mino_2P = -1
                    bottom_count_2P = 0
                    hard_drop_2P = False
                    attack_point = 0
                    attack_point_2P = 0
                    score_2P = 0
                    level_2P = 1
                    goal_2P = level_2P * 5
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]
                    pvp_over = False
                    player = 0
                    attack_stack = 0
                    attack_stack_2P = 0
                    erase_stack = 0
                    erase_stack_2P = 0                     
                pygame.display.flip()
                pygame.key.set_repeat(0)
                
            
    # pvp game over screen
    elif pvp_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2_b.render("GAME", 1, ui_variables.white)
                over_text_2 = ui_variables.h2_b.render("OVER", 1, ui_variables.white)
                over_start = ui_variables.h5.render("Press Enter to main page", 1, ui_variables.white)

                draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                screen.blit(over_text_1, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.167))
                screen.blit(over_text_2, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.233))
                screen.blit(over_start, (SCREEN_WIDTH * 0.033, SCREEN_HEIGHT * 0.3333))

                # win-lose 이미지 출력
                if player == 1:
                    screen.blit(pygame.transform.scale(ui_variables.pvp_win_image,
                                                       (
                                                           int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.6))),
                                (int(SCREEN_WIDTH * 0.08), int(SCREEN_HEIGHT * 0.3)))
                    screen.blit(pygame.transform.scale(ui_variables.pvp_lose_image,
                                                       (
                                                           int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.6))),
                                (int(SCREEN_WIDTH * 0.55), int(SCREEN_HEIGHT * 0.3)))
                elif player == 2:
                    screen.blit(pygame.transform.scale(ui_variables.pvp_lose_image,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.6))),
                                (int(SCREEN_WIDTH * 0.08), int(SCREEN_HEIGHT * 0.3)))
                    screen.blit(pygame.transform.scale(ui_variables.pvp_win_image,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.6))),
                                (int(SCREEN_WIDTH * 0.55), int(SCREEN_HEIGHT * 0.3)))
                pygame.display.update()

            # 마우스로 창크기조절
            elif event.type == VIDEORESIZE:

                SCREEN_WIDTH = event.w

                SCREEN_HEIGHT = event.h

                if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                    SCREEN_WIDTH = min_width

                    SCREEN_HEIGHT = min_height

                if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                        board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                    SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                    SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                pygame.display.update()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()
                    page, selected = MENU_PAGE, 0 
                    width = DEFAULT_WIDTH  # Board width
                    height = DEFAULT_HEIGHT
                    game_over = False
                    reverse_over = False
                    item_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    fever_score = 500
                    max_score = 99999
                    score = 0
                    next_fever = 500
                    fever_interval = 3
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]
                    set_difficulty = 0

                    

                    min_width = 700
                    min_height = 350
                    board_rate = 0.5

                    # PvP모드
                    hold_2P = False
                    dx_2P, dy_2P = 3, 0
                    rotation_2P = 0
                    mino_2P = randint(1, 7)
                    next_mino_2P = randint(1, 7)
                    hold_mino_2P = -1
                    bottom_count_2P = 0
                    hard_drop_2P = False
                    attack_point = 0
                    attack_point_2P = 0
                    score_2P = 0
                    level_2P = 1
                    goal_2P = level_2P * 5
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]
                    pvp_over = False
                    player = 0
                    attack_stack = 0
                    attack_stack_2P = 0
                    erase_stack = 0
                    erase_stack_2P = 0
            
    # Start screen
    else:
        # 복잡성을 줄이기 위해 start screen 내부에 page를 나누는 방식으로 구현했습니다.
        # Start page <-> Menu Page <-> Mode Page <-> Diffculty Page -> Start
        #                          <-> Help Page
        #                          <-> Setting Page
        #
        # page는 지금 있는 page의 고유 넘버를 나타내고, 아래와 같이 상수를 사용해 가독성을 높였습니다.
        # selected는 선택지가 있는 페이지에서 몇번째  보기를 선택하고 있는지 나타내는 변수입니다.
        # 편의상 0부터 시작합니다.

        START_PAGE, MENU_PAGE, HELP_PAGE, SETTING_PAGE, MODE_PAGE, DIFFICULTY_PAGE = 0, 10, 11, 12, 20, 30
        page, selected = START_PAGE, 0
        if background_music:
            ui_variables.background_sound.play()
            background_music = False

        while not done and not start and not reverse and not pvp and not item:
            # Start Page
            if page == START_PAGE:              
                text_surf = ui_variables.h2_i.render(text, True, (0,0,0))
                pass_surf = ui_variables.h2_i.render('*'* len(password), True, (0, 0, 0))
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        ## 아이디 입력
                        if event.key == pygame.K_BACKSPACE:
                            if IDchoice == True:
                                text = text[:-1]                               
                                text_surf = ui_variables.h2_i.render(text, True, (0,0,0))
                            elif Passchoice == True:
                                IDchoice == False
                                password = password[:-1]
                                pass_surf = ui_variables.h2_i.render('*'* len(password), True, (0, 0, 0)) 
                        elif event.key == K_SPACE:
                            pass
                        elif event.key == K_TAB:
                            pass
                        elif event.key == K_RETURN:  ## enter 인듯
                            pygame.key.set_repeat(0)
                            ui_variables.click_sound.play()
                            if LoginCom(text,"PLAYER",password):
                                pygame.time.delay(100)
                               
                                ui_variables.loginText = "SUCESS" 
                                SavedID = text
                                SavedPass = password    
                                page, selected = MENU_PAGE,0
                            elif LoginID("PLAYER",text) == False:
                                ui_variables.loginText = "NEW PLAYER"  
                                if password =="":
                                    break
                                SavedID = text
                                SavedPass = password 
                                page, selected = MENU_PAGE,0
                                
                            elif LoginID("PLAYER",text) == True and LoginPass(text,"PLAYER",password) == False:
                                ui_variables.loginText = "PASSWORD FAIL"  
                                
                                page, selected = START_PAGE,0
                        
                        else:
                            if IDchoice == True:
                                Passchoice == False
                                text += event.unicode 
                                text_surf = ui_variables.h2_i.render(text, True, (0, 0, 0))
                            elif Passchoice == True:
                                IDchoice == False
                                password += event.unicode
                                pass_surf = ui_variables.h2_i.render('*'* len(password), True, (0, 0, 0)) 
                                
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if id_box.collidepoint(event.pos):
                            IDchoice = not IDchoice
                            text=""
                            text_surf = ui_variables.h2_i.render(text, True, (0, 0, 0))
                        elif pass_box.collidepoint(event.pos):
                            IDchoice = not IDchoice
                            IDchoice = False
                            Passchoice = not Passchoice
                            password = ""
                            pass_surf = ui_variables.h2_i.render('*'* len(password), True, (0, 0, 0))   
                                      
                    elif event.type == VIDEORESIZE:
                        time.sleep(1)
                        SCREEN_WIDTH = event.w

                        SCREEN_HEIGHT = event.h

                        if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                            SCREEN_WIDTH = min_width

                            SCREEN_HEIGHT = min_height

                        if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                                board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                            SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                            SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                        block_size = int(SCREEN_HEIGHT * 0.045)
                        inven_size = int(SCREEN_HEIGHT * 0.08)
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        barrier_size = int(SCREEN_HEIGHT * 0.9)
                    
                        
                           
                
                
                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                screen.fill(ui_variables.white)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    Rect(0, 0, int(SCREEN_WIDTH), int(SCREEN_HEIGHT * 0.24))
                )

                title = ui_variables.h1_s.render("TTOTRIS™", 1, ui_variables.white)
                login = ui_variables.h1.render("ID", 1, ui_variables.grey_1)
                passwordScreen = ui_variables.h1.render("PassWord", 1, ui_variables.grey_1)
                ID = ui_variables.h2.render("ID", 1, ui_variables.grey_1)
                PASSWORD = ui_variables.h2.render("PASSWORD", 1, ui_variables.grey_1)
                title_menu = ui_variables.h5.render("INSERT ID  and  PASSWORD", 1, ui_variables.grey_1)
                pressEnter = ui_variables.h5.render(" Then Press Enter to Start", 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Copyright (c) 2021 DOITDOIT Rights Reserved.", 1, ui_variables.grey_1)
                
                if blink:
                    screen.blit(title_menu, title.get_rect(center=(int(SCREEN_WIDTH / 1.95), int(SCREEN_HEIGHT * 0.45))))
                    screen.blit(pressEnter, title.get_rect(center=(int(SCREEN_WIDTH / 1.95), int(SCREEN_HEIGHT * 0.5))))
                blink = not blink

                screen.blit(ID, ID.get_rect(center=(SCREEN_WIDTH / 2.3, SCREEN_HEIGHT * 1.8)))
                id_box = pygame.Rect(SCREEN_WIDTH / 2.3, SCREEN_HEIGHT / 1.9, 140, 32)
                pass_box = pygame.Rect(SCREEN_WIDTH / 2.3, SCREEN_HEIGHT / 1.6, 140, 32)
                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2.5, SCREEN_HEIGHT * 1.9)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))
                screen.blit(login,(int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT * 2)))
                screen.blit(text_surf, (id_box.x+5,id_box.y+5))
                screen.blit(pass_surf, (pass_box.x+5,pass_box.y+7)) 
                IDcolor = color_IDactive if IDchoice else color_inIDactive
                Passcolor = color_Passactive if Passchoice else color_inPassactive
                window_center = screen.get_rect().center          
                pygame.draw.rect(screen, IDcolor, id_box, 2)
                pygame.draw.rect(screen, Passcolor, pass_box, 2)
                loginText = ui_variables.h1.render(ui_variables.loginText,1,ui_variables.black)
                screen.blit(loginText,loginText.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT /3.3)))
                ui_variables.loginText =""              
                pygame.display.flip()
            
            # MENU PAGE
            elif page == MENU_PAGE:
                current_selected = selected
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.key.set_repeat(0)
                            # back to start page
                            ui_variables.click_sound.play()
                            page, selected = START_PAGE, 0
                        elif event.key == K_DOWN:
                            pygame.key.set_repeat(0)
                            if selected == 0 or selected == 1: # 마지막 선택지가 아니면
                                # next menu select
                                ui_variables.click_sound.play()
                                selected = selected + 1 # 다음 선택지로
                        elif event.key == K_UP:
                            pygame.key.set_repeat(0)
                            if selected == 1 or selected == 2: # 첫 선택지가 아니면
                                # previous menu select
                                ui_variables.click_sound.play()
                                selected = selected - 1 # 이전 선택지로
                        elif event.key == K_SPACE: # 선택
                            pygame.key.set_repeat(0)
                            if selected == 0: 
                                # select start menu, goto mode select page
                                ui_variables.click_sound.play()
                                page, selected = MODE_PAGE, 0
                            elif selected == 1:
                                # select help menu, goto help page
                                ui_variables.click_sound.play()
                                page, selected = HELP_PAGE, 0
                            elif selected == 2:
                                # select settings menu, goto settings menu
                                ui_variables.click_sound.play()
                                page, selected = SETTING_PAGE, 0
                    # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:
                        time.sleep(1)
                        SCREEN_WIDTH = event.w

                        SCREEN_HEIGHT = event.h

                        if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                            SCREEN_WIDTH = min_width

                            SCREEN_HEIGHT = min_height

                        if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                                board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                            SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                            SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                        block_size = int(SCREEN_HEIGHT * 0.045)
                        inven_size = int(SCREEN_HEIGHT * 0.08)
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        barrier_size = int(SCREEN_HEIGHT * 0.9)
                
                screen.fill(ui_variables.white)
                block_size = int(SCREEN_HEIGHT * 0.9)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    Rect(0, 0, int(SCREEN_WIDTH),
                         int(SCREEN_HEIGHT * 0.24))
                )

                title = ui_variables.h1_s.render("TTOTRIS™", 1, ui_variables.white)
                title_info = ui_variables.h6.render("Press up and down to change, space to select", 1,
                                                    ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)))

                title_start = ui_variables.h5.render("Game start", 1, ui_variables.grey_1)
                title_help = ui_variables.h5.render("Help", 1, ui_variables.grey_1)
                title_setting = ui_variables.h5.render("Settings", 1, ui_variables.grey_1)

                pos_start = title_start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
                pos_help = title_help.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
                pos_setting = title_setting.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

                # blink current selected option
                if blink:
                    if current_selected == 0:
                        screen.blit(title_help, pos_help)
                        screen.blit(title_setting, pos_setting)
                    elif current_selected == 1:
                        screen.blit(title_start, pos_start)
                        screen.blit(title_setting, pos_setting)
                    else:
                        screen.blit(title_start, pos_start)
                        screen.blit(title_help, pos_help)
                else:
                    screen.blit(title_start, pos_start)
                    screen.blit(title_help, pos_help)
                    screen.blit(title_setting, pos_setting)

                blink = not blink

            # HELP PAGE
            elif page == HELP_PAGE:
                current_selected = selected
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        # back to menu page
                        if event.key == K_ESCAPE:
                            pygame.key.set_repeat(0)
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
                        elif event.key == K_RIGHT:
                            pygame.key.set_repeat(0)
                            if selected == 0:
                                ui_variables.click_sound.play()
                                selected = selected + 1
                        elif event.key == K_LEFT:
                            pygame.key.set_repeat(0)
                            if selected > 0:
                                # previous difficulty select
                                ui_variables.click_sound.play()
                                selected = selected - 1
                        
                        

                        

                    # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:

                        SCREEN_WIDTH = event.w

                        SCREEN_HEIGHT = event.h

                        if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                            SCREEN_WIDTH = min_width

                            SCREEN_HEIGHT = min_height

                        if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                                board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                            SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                            SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                        block_size = int(SCREEN_HEIGHT * 0.045)
                        inven_size = int(SCREEN_HEIGHT * 0.08)
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        barrier_size = int(SCREEN_HEIGHT * 0.9)
                       
                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    pygame.draw.rect(
                        screen,
                        ui_variables.grey_1,
                        Rect(0, 0, int(SCREEN_WIDTH),
                             int(SCREEN_HEIGHT * 0.24))
                    )
                )

                title = ui_variables.h1_s.render("HELP", 1, ui_variables.white)
                title_info = ui_variables.h6.render("Press esc to return menu", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                keyhelp_img = pygame.transform.scale(pygame.image.load(ui_variables.help_key), (SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.7))
                keyhelp_r = keyhelp_img.get_rect()
                keyhelp_r.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.62)

                itemhelp_img = pygame.transform.scale(pygame.image.load(ui_variables.help_item), (SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.7))
                itemhelp_r = itemhelp_img.get_rect()
                itemhelp_r.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.62)
                
                if current_selected == 0:
                    screen.blit(keyhelp_img, keyhelp_img.get_rect(center=keyhelp_r.center))
                    pos = [[SCREEN_WIDTH - 10, SCREEN_HEIGHT / 2], [SCREEN_WIDTH - 15, SCREEN_HEIGHT / 2 - 5],
                           [SCREEN_WIDTH - 15, SCREEN_HEIGHT / 2 + 5]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)
                else:
                    screen.blit(itemhelp_img, itemhelp_img.get_rect(center=itemhelp_r.center))
                    pos = [[10, SCREEN_HEIGHT / 2], [15, SCREEN_HEIGHT / 2 - 5], [15, SCREEN_HEIGHT / 2 + 5]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)

              

            # Setting Page
            elif page == SETTING_PAGE:
                current_selected = selected
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.key.set_repeat(0)
                            # back to start page
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
                        elif event.key == K_DOWN:
                            pygame.key.set_repeat(0)
                            if selected == 0 or selected == 1 or selected == 2:
                                # next menu select
                                ui_variables.click_sound.play()
                                selected = selected + 1
                        elif event.key == K_UP:
                            pygame.key.set_repeat(0)
                            if selected == 1 or selected == 2 or selected == 3:
                                # previous menu select
                                ui_variables.click_sound.play()
                                selected = selected - 1
                        elif event.key == K_SPACE:
                            pygame.key.set_repeat(0)
                            if selected == 0:
                                # 미니 사이즈
                                ui_variables.click_sound.play()
                                SCREEN_WIDTH = 800
                                SCREEN_HEIGHT = 400
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                                pygame.display.update()
                                # page, selected = DIFFICULTY_PAGE, 0
                            elif selected == 1:
                                # 중간 사이즈
                                ui_variables.click_sound.play()
                                SCREEN_WIDTH = 1200
                                SCREEN_HEIGHT = 600
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                                pygame.display.update()
                            # page = HELP_PAGE
                            elif selected == 2:
                                # 큰 사이즈
                                ui_variables.click_sound.play()
                                SCREEN_WIDTH = 1600
                                SCREEN_HEIGHT = 800
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                                pygame.display.update()
                                # page = SETTING_PAGE
                        elif event.key == K_LEFT:
                            pygame.key.set_repeat(0)
                            if selected == 3:
                                ui_variables.click_sound.play()
                                if effect_volume <= 0:
                                    effect_volume = 0
                                else:
                                    effect_volume -= 1

                        elif event.key == K_RIGHT:
                            pygame.key.set_repeat(0)
                            if selected == 3:
                                ui_variables.click_sound.play()
                                if effect_volume >= 10:
                                    effect_volume = 10
                                else:
                                    effect_volume += 1
                        set_volume()

                    # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:

                        SCREEN_WIDTH = event.w

                        SCREEN_HEIGHT = event.h

                        if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                            SCREEN_WIDTH = min_width

                            SCREEN_HEIGHT = min_height

                        if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                                board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                            SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                            SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                        block_size = int(SCREEN_HEIGHT * 0.045)
                        inven_size = int(SCREEN_HEIGHT * 0.08)
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        barrier_size = int(SCREEN_HEIGHT * 0.9)
                
                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                screen.fill(ui_variables.white)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    pygame.draw.rect(
                        screen,
                        ui_variables.grey_1,
                        Rect(0, 0, int(SCREEN_WIDTH),
                             int(SCREEN_HEIGHT * 0.24))
                    )
                )

                title = ui_variables.h1_s.render("SETTINGS", 1, ui_variables.white)

                title_info = ui_variables.h6.render("Press esc to return menu", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))

                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220)))

                screen_size = ui_variables.h2.render("SCREEN SIZE", 1, ui_variables.grey_1)
                screen.blit(screen_size, screen_size.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60)))
                volume = ui_variables.h2.render("VOLUME", 1, ui_variables.grey_1)
                screen.blit(volume, volume.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120)))

                mini_size = ui_variables.h5.render("800 X 400", 1, ui_variables.grey_1)
                medium_size = ui_variables.h5.render("1200 X 600", 1, ui_variables.grey_1)
                full_size = ui_variables.h5.render("1600 X 800", 1, ui_variables.grey_1)
                sound = ui_variables.h5.render(str(effect_volume), 1, ui_variables.grey_1)

                pos_mini_size = mini_size.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
                pos_medium_size = medium_size.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
                pos_full_size = full_size.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
                pos_sound = sound.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 160))

                if effect_volume > 0:
                    pos = [[SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 + 160],
                           [SCREEN_WIDTH / 2 - 25, SCREEN_HEIGHT / 2 + 155],
                           [SCREEN_WIDTH / 2 - 25, SCREEN_HEIGHT / 2 + 165]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)

                if effect_volume < 10:
                    pos = [[SCREEN_WIDTH / 2 + 30, SCREEN_HEIGHT / 2 + 160],
                           [SCREEN_WIDTH / 2 + 25, SCREEN_HEIGHT / 2 + 155],
                           [SCREEN_WIDTH / 2 + 25, SCREEN_HEIGHT / 2 + 165]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)

                # blink current selected option
                if blink:
                    if current_selected == 0:
                        screen.blit(medium_size, pos_medium_size)
                        screen.blit(full_size, pos_full_size)
                        screen.blit(sound, pos_sound)
                    elif current_selected == 1:
                        screen.blit(mini_size, pos_mini_size)
                        screen.blit(full_size, pos_full_size)
                        screen.blit(sound, pos_sound)
                    elif current_selected == 2:
                        screen.blit(mini_size, pos_mini_size)
                        screen.blit(medium_size, pos_medium_size)
                        screen.blit(sound, pos_sound)
                    else:
                        screen.blit(mini_size, pos_mini_size)
                        screen.blit(medium_size, pos_medium_size)
                        screen.blit(full_size, pos_full_size)
                else:
                    screen.blit(mini_size, pos_mini_size)
                    screen.blit(medium_size, pos_medium_size)
                    screen.blit(full_size, pos_full_size)
                    screen.blit(sound, pos_sound)

                blink = not blink

            # 여기가  MODE PAGE. 
            elif page == MODE_PAGE:
                # 모드를 설정한다.
                DIFFICULTY_COUNT = 5
                DIFFICULTY_NAMES = ["NORMAL", "HARD","PVP", "ITEM", "REVERSE"]
                DIFFICULTY_EXPLAINES = [
                    "Noraml tetris mode",
                    "Can you play Tetris while overcoming obstacles? ",
                    "Player versus Player",
                    "Some items will be appeared in game",
                    "Can you play Tetris with reversed direction keys?"
                ]
                set_difficulty = 0
                current_selected = selected
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.key.set_repeat(0)
                            # back to menu page
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
                        elif event.key == K_RIGHT:
                            pygame.key.set_repeat(0)
                            if selected < DIFFICULTY_COUNT - 1:
                                # next difficulty select
                                ui_variables.click_sound.play()
                                selected = selected + 1
                        elif event.key == K_LEFT:
                            pygame.key.set_repeat(0)
                            if selected > 0:
                                # previous difficulty select
                                ui_variables.click_sound.play()
                                selected = selected - 1
                        
                        mode_selected = selected   # 현재 선택한 모드 저장        
                        
                        if event.key == K_SPACE: # -> DIFFICULTY PAGE로 가도록
                            pygame.key.set_repeat(0)
                            ui_variables.click_sound.play()
                            page,selected = DIFFICULTY_PAGE, 0
                        


                    # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:

                        SCREEN_WIDTH = event.w

                        SCREEN_HEIGHT = event.h

                        if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                            SCREEN_WIDTH = min_width

                            SCREEN_HEIGHT = min_height

                        if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                                board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                            SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                            SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                        block_size = int(SCREEN_HEIGHT * 0.045)
                        inven_size = int(SCREEN_HEIGHT * 0.08)
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        barrier_size = int(SCREEN_HEIGHT * 0.9)
                
                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                screen.fill(ui_variables.white)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    pygame.draw.rect(
                        screen,
                        ui_variables.grey_1,
                        Rect(0, 0, int(SCREEN_WIDTH),
                             int(SCREEN_HEIGHT * 0.24))
                    )
                )
                ## 여기에 모드별 점수를 blit
                font2 = pygame.font.Font("./assets/fonts/OpenSans-Semibold.ttf", 15)
                #font2 = pygame.font.Font('assets/fonts/NanumGothicCoding-Bold.ttf', 15)
                difficulty_name = DIFFICULTY_NAMES[current_selected]
                difficulty_explain = DIFFICULTY_EXPLAINES[current_selected]
                 
                if DIFFICULTY_NAMES[current_selected] == "NORMAL":
                    cursor = tetris.cursor()
                    sql = "SELECT COUNT(id) FROM NORMAL"
                    cursor.execute(sql)
                    num = cursor.fetchone()
                    for i in range(int(num[0])):
                        if i > 2: 
                            continue
                        query = "SELECT * FROM NORMAL ORDER BY score DESC"
                        cursor.execute(query)
                        datas = cursor.fetchmany(size =int(num[0]))
                        ScoreBoard = font2.render(''.join(str(i+1)+'st  '+str(datas[i][0])+'   '+str(datas[i][1])), 1, ui_variables.white)
                        screen.blit(ScoreBoard, ScoreBoard.get_rect(center=(SCREEN_WIDTH / 11, ((SCREEN_HEIGHT * 0.05*(i+1))))))
                if DIFFICULTY_NAMES[current_selected] == "HARD":
                    cursor = tetris.cursor()
                    sql = "SELECT COUNT(id) FROM HARD"
                    cursor.execute(sql)
                    num = cursor.fetchone()
                    for i in range(int(num[0])):
                        if i > 2: 
                            continue
                        query = "SELECT * FROM HARD ORDER BY score DESC"
                        cursor.execute(query)
                        datas = cursor.fetchmany(size =int(num[0]))
                        ScoreBoard = font2.render(''.join(str(i+1)+'st  '+str(datas[i][0])+'   '+str(datas[i][1])), 1, ui_variables.white)
                        screen.blit(ScoreBoard, ScoreBoard.get_rect(center=(SCREEN_WIDTH / 11, ((SCREEN_HEIGHT * 0.05*(i+1))))))     
                if DIFFICULTY_NAMES[current_selected] == "ITEM":
                    cursor = tetris.cursor()
                    sql = "SELECT COUNT(id) FROM ITEM"
                    cursor.execute(sql)
                    num = cursor.fetchone()
                    for i in range(int(num[0])):
                        if i > 2: 
                            continue
                        query = "SELECT * FROM ITEM ORDER BY score DESC"
                        cursor.execute(query)
                        datas = cursor.fetchmany(size =int(num[0]))
                        ScoreBoard = font2.render(''.join(str(i+1)+'st  '+str(datas[i][0])+'   '+str(datas[i][1])), 1, ui_variables.white)
                        screen.blit(ScoreBoard, ScoreBoard.get_rect(center=(SCREEN_WIDTH / 11, ((SCREEN_HEIGHT * 0.05*(i+1))))))
                if DIFFICULTY_NAMES[current_selected] == "REVERSE":
                    cursor = tetris.cursor()
                    sql = "SELECT COUNT(id) FROM REVERSE"
                    cursor.execute(sql)
                    num = cursor.fetchone()
                    for i in range(int(num[0])):
                        if i > 2: 
                            continue
                        query = "SELECT * FROM REVERSE ORDER BY score DESC"
                        cursor.execute(query)
                        datas = cursor.fetchmany(size =int(num[0]))
                        ScoreBoard = font2.render(''.join(str(i+1)+'st  '+str(datas[i][0])+'   '+str(datas[i][1])), 1, ui_variables.white)
                        screen.blit(ScoreBoard, ScoreBoard.get_rect(center=(SCREEN_WIDTH / 11, ((SCREEN_HEIGHT * 0.05*(i+1))))))
                
                title = ui_variables.h1_s.render(difficulty_name, 1, ui_variables.white)
                title_explain = font2.render(difficulty_explain, 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Press left and right to change, space to select difficulty", 1,
                                                    ui_variables.grey_1)
            
                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_explain, title_explain.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                # draw left, right sign (triangle)
                if current_selected > 0:
                    pos = [[10, SCREEN_HEIGHT / 2], [15, SCREEN_HEIGHT / 2 - 5], [15, SCREEN_HEIGHT / 2 + 5]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)

                if current_selected < DIFFICULTY_COUNT - 1:
                    pos = [[SCREEN_WIDTH - 10, SCREEN_HEIGHT / 2], [SCREEN_WIDTH - 15, SCREEN_HEIGHT / 2 - 5],
                           [SCREEN_WIDTH - 15, SCREEN_HEIGHT / 2 + 5]]
                    pygame.draw.polygon(screen, ui_variables.grey_1, pos, 1)
            
            elif page == DIFFICULTY_PAGE:
                # current_selected = selected 
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.key.set_repeat(0)
                            ui_variables.click_sound.play()
                            page, selected = MODE_PAGE, mode_selected # 모드 선택 페이지로, 원래 선택했던 모드 화면이 뜸
                            
                        elif event.key == K_UP:
                            pygame.key.set_repeat(0)
                            ui_variables.click_sound.play()
                            if set_difficulty >= 9: 
                                set_difficulty = 9
                            else:
                                set_difficulty += 1
                            
                        elif event.key == K_DOWN:
                            pygame.key.set_repeat(0)
                            ui_variables.click_sound.play()
                            if set_difficulty <= 0:
                                set_difficulty = 0
                            else:
                                set_difficulty -= 1
                            pygame.draw.polygon(screen, ui_variables.black, pos, 0)

                        if event.key == K_SPACE:
                            pygame.key.set_repeat(0)
                            # mode page에서 선택된 모드
                            if mode_selected ==0: #normal mode
                                # start game with selected difficulty
                                ui_variables.click_sound.play()
                                start = True
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, mode_selected, set_difficulty)

                            if mode_selected == 1: # hard mode 
                                ui_variables.click_sound.play()
                                hard = True
                                start = True 
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, mode_selected, set_difficulty)

                            if mode_selected == 2: # pvp mode
                                ui_variables.click_sound.play()
                                pvp = True
                                start = False
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, mode_selected, set_difficulty)

                            if mode_selected == 3: # item mode
                                # start game with ITEM
                                ui_variables.click_sound.play()
                                start = True
                                item = True 
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, mode_selected, set_difficulty)
    
                            if mode_selected == 4: # Reverse mode 
                                ui_variables.click_sound.play()
                                start = True
                                reverse = True
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, mode_selected, set_difficulty)
                                
                         # 마우스로 창크기조절
                    elif event.type == VIDEORESIZE:

                        SCREEN_WIDTH = event.w

                        SCREEN_HEIGHT = event.h

                        if SCREEN_WIDTH < min_width or SCREEN_HEIGHT < min_height:  # 최소 너비 또는 높이를 설정하려는 경우

                            SCREEN_WIDTH = min_width

                            SCREEN_HEIGHT = min_height

                        if not ((board_rate - 0.1) < (SCREEN_HEIGHT / SCREEN_WIDTH) < (

                                board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면

                            SCREEN_WIDTH = int(SCREEN_HEIGHT / board_rate)  # 너비를 적정 비율로 바꿔줌

                            SCREEN_HEIGHT = int(SCREEN_WIDTH * board_rate)  # 높이를 적정 비율로 바꿔줌

                        block_size = int(SCREEN_HEIGHT * 0.045)
                        inven_size = int(SCREEN_HEIGHT * 0.08)
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        barrier_size = int(SCREEN_HEIGHT * 0.9)
                        
                block_size = int(SCREEN_HEIGHT * 0.045)
                inven_size = int(SCREEN_HEIGHT * 0.08)
                screen.fill(ui_variables.white)
                barrier_size = int(SCREEN_HEIGHT * 0.9)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    pygame.draw.rect(
                        screen,
                        ui_variables.grey_1,
                        Rect(0, 0, int(SCREEN_WIDTH),
                             int(SCREEN_HEIGHT * 0.24))
                    )
                )
                title = ui_variables.h1_s.render("DIFFICULTY", 1, ui_variables.white)

                title_info1 = ui_variables.h6.render("Press up and down to change speed, space to start game", 1, ui_variables.grey_1)
                title_info2 = ui_variables.h6.render("Press esc to return to mode page", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))

                screen.blit(title_info1, title_info1.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200)))
                screen.blit(title_info2, title_info2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220)))
    
                
                
                velocity = ui_variables.h2.render(str(set_difficulty), 1, ui_variables.black)
                pos_velocity = velocity.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 15 ))
                screen.blit(velocity, pos_velocity)
                
                if set_difficulty > 0: # 0 이하이면 아래쪽 삼각형 안 보이게 하려는 조건
                    pos = [[SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2 + 90],
                           [SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 + 60],
                           [SCREEN_WIDTH / 2 + 30, SCREEN_HEIGHT / 2 + 60]]
                    pygame.draw.polygon(screen, ui_variables.black, pos, 0) # 원하는 좌표에 삼각형 그리기

                if set_difficulty < 9: # 9 이상이면 위쪽 삼각형 안 보이게 하려는 조건
                    pos = [[SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2 - 60],
                           [SCREEN_WIDTH / 2 - 30 , SCREEN_HEIGHT / 2 - 30],
                           [SCREEN_WIDTH / 2 + 30, SCREEN_HEIGHT / 2 - 30]]
                    pygame.draw.polygon(screen, ui_variables.black, pos, 0) 
                
                
               
            if not start:
                pygame.display.update()
                clock.tick(3)
pygame.quit()