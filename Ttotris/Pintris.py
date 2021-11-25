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

# Constants 안 변하는 것들
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600


FRAMERATE_MULTIFLIER_BY_DIFFCULTY = [0.9, 0.8, 0.9, 0.9, 0.9] # pvp, item, reverse는 normal과 같은 비율
DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 20

# Define
block_size = 17  # Height, width of single block
width = DEFAULT_WIDTH  # Board width
height = DEFAULT_HEIGHT  # Board height
c =0
mino_size = 4
mino_turn = 4
fever = False

color_active = pygame.Color('lightskyblue3')
color_inactive = pygame.Color('blue')
color = color_inactive
framerate = 30  # Bigger -> Slower
barPos      = (650, 200)
barSize     = (250, 20)
borderColor = (0, 0, 0)
barColor    = (0, 128, 0)
min_width = 700
min_height = 350
board_rate = 0.5
text = ""
input_active = True
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


# Draw block 
def draw_block(x, y, color): 
    if color == ui_variables.t_color[row_mino]:
        draw_image(screen, ui_variables.row_iamge, x,y, block_size, block_size ) # 아이템 블록은 이미지로, row_item
    elif color == ui_variables.t_color[col_mino]:
        draw_image(screen, ui_variables.col_iamge, x, y, block_size, block_size ) # 아이템 블록은 이미지로, col_item
    elif color == ui_variables.t_color[bomb_mino]:
        draw_image(screen, ui_variables.bomb_iamge, x,y, block_size, block_size ) # 아이템 블록은 이미지로, bomb_item
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
    x = x - (w / 2) #해당 이미지의 가운데 x좌표, 가운데 좌표이기 때문에 2로 나눔
    y = y - (h / 2) #해당 이미지의 가운데 y좌표, 가운데 좌표이기 때문에 2로 나눔
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
    screen.blit(text_fever, text_fever.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.2780))))

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
                draw_block_image(dx,dy,ui_variables.t_block[grid_n[i][j]]) # 블록 이미지 출력
                # pygame.draw.rect(
                #     screen,
                #     ui_variables.t_color[grid_n[i][j]],
                #     Rect(dx, dy, block_size, block_size)
                # )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(mino_size):
            for j in range(mino_turn):
                dx = int(SCREEN_WIDTH * 0.025) + sidebar_width + block_size * j
                dy = int(SCREEN_HEIGHT * 0.1) + block_size * i
                if grid_h[i][j] != 0:
                    draw_block_image(dx,dy,ui_variables.t_block[grid_h[i][j]]) # 블록 이미지 출력
                #     pygame.draw.rect(
                #     screen,
                #     ui_variables.t_color[grid_h[i][j]],
                #     Rect(dx, dy, block_size, block_size)
                # )

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
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.15) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_score, text_score.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5187))))
    screen.blit(score_value, score_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.5614))))
    screen.blit(text_level, text_level.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.6791))))
    screen.blit(level_value, level_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.7219))))
    screen.blit(text_goal, text_goal.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8395))))
    screen.blit(goal_value, goal_value.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.8823))))
    screen.blit(text_item, text_item.get_rect(center=(int(SCREEN_WIDTH * 0.2375/ 2) + sidebar_width, int(SCREEN_HEIGHT * 0.2780))))

    
     
    show_inven() # 아이템이 있으면 아이템 이미지 출력

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

    # Erase ghost
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
def istheresaved(name2,table):
    if isthereID(name2,table):
        cursor = tetris.cursor()
        sql = "INSERT INTO {} (id, score) VALUES (%s,%s)".format(table)
        cursor.execute(sql, (name2, score))
        tetris.commit()  
        cursor.close() ## tetris db insert 
    else :      
        cursor = tetris.cursor()
        sql = "select score from {} where id =%s".format(table)
        cursor.execute(sql, name2)
        result = cursor.fetchone()
        if result[0] < score:                           
            sql = "Update {} set score = %s where id =%s".format(table)
            cursor.execute(sql, (score,name2))
            tetris.commit()  
            cursor.close() ## tetris db insert 
        else: pass

def DrawBar(pos, size, borderC, barC, progress):
    
    pygame.draw.rect(screen, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+3, pos[1]+3)
    innerSize = ((size[0]-6) * progress, size[1]-6)
    pygame.draw.rect(screen, barC, (*innerPos, *innerSize))


# 아이템 획득~인벤토리 관련 함수 
def get_item():
    if len(inven)<3:
        inven.append(item_list [randrange(0,5)]) # 랜덤으로 얻음

def show_inven():
    if len(inven) != 0:
        for i in range(len(inven)):
            item = inven[i]
            screen.blit(item, item.get_rect(center=(dx_inven[i],dy_inven))) # 인벤에 들어간 아이템 이미지 출력
    else: # 없을 때는 빈 정사각형 출력
        pygame.draw.rect(screen,ui_variables.black, (dx_inven[0]-item_size/2, dy_inven-item_size/2, item_size,item_size),1)
        pygame.draw.rect(screen,ui_variables.black, (dx_inven[1]-item_size/2, dy_inven-item_size/2, item_size,item_size),1)
        pygame.draw.rect(screen,ui_variables.black, (dx_inven[2]-item_size/2, dy_inven-item_size/2, item_size,item_size),1)

def use_item(key): # 사용자의 키조작 전달 받기
    if len(inven)>0:
        item_u = inven[key-1] # 인벤토리의 key번째 칸 아이템
        inven.pop(key-1) # 사용한 아이템은 삭제
        # # 해당 아이템 블록 번호 저장
        # if item == row_inven: 
        #     num_item = row_mino
        # elif item == col_inven:
        #     num_item = col_mino
        # elif item == bomb_inven:
        #     num_item = bomb_mino
        # else:
     #     num_item = no_mino

    #     return {

    #     }
    return item_u

    
    

# 아이템 사용 함수
def earthquake(): # 맨 아래 줄 삭제 아이템
    for i in range(width): # 가로줄 전체에 대해서
        matrix[i][height] = 0 
    k = height+1 
    while k > 0:  # 남아있는 블록 아래로 한 줄씩 내리기
        for i in range(width):
            matrix[i][k] = matrix[i][k-1]
        k -= 1       
    # 사용하고 나면, score += 50 * level # 한 줄 지운 것과 같은 효과 주기

def board_reset():
    for j in range(height+1):
        for i in range(width):
            matrix[i][j] = 0 # 보드 내 블록 다 비워버리기

def erase_row():    # 가로줄 삭제 아이템 효과
    for j in range(height+1):
        for i in range(width):
            if matrix[i][j] == row_mino: # i_row 블록이면
                k = j # y 좌표 기억
                matrix[i][k] = 0 # 해당 줄 삭제
                while k>0: 
                    for i in range(width):
                        matrix[i][k] = matrix[i][k-1] # 지워진 줄 위에 있던 블록 한 줄씩 내리기
                    k -= 1

def erase_col(): # 세로줄 삭제 아이템 효과
    for j in range(height+1):
        for i in range(width):
            if matrix[i][j] == col_mino: # i_col 블록이면
                k = i # x 좌표 기억
                matrix[k][j] = 0 # i_col 블록이 위치한 세로줄 삭제

def bomb():# 3x3 블록 삭제 아이템 효과
    for j in range(height+1):
        for i in range(width):
            if matrix[i][j] == bomb_mino: # i_bomb 블록이면
                m = i-1 # 3x3 블록 없애주니까 i-1 ~ i+1 번째 지위져야 함
                n = j -1
                for k in range(bomb_size): # 3x3이므로
                    for q in range(bomb_size): # 
                        if m+k >= 0 and n+q >= 0: # 블록이 있든 없든
                            matrix[m+k][n+q] = 0 # 3x3만큼 다 지워줌


            




# Start game
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 7)
pygame.display.set_caption("TTOTRIS™")
text = ""
font3 = pygame.font.Font('assets/fonts/NanumGothicCoding-Bold.ttf', 40)
text_surf = font3.render(text, True, (0, 0, 0)) 

# pages
blink = False
blink1 = False
blink2 = False
blink3 = False
start = False
# hard
hard = False
pause = False
done = False
game_over = False
reverse = False
pvp = False
reverse_over = False
pvp_over = False
item = False
item_over = False

# Initial values
speed_change=2 # 게임 시작 시 difficulty에 곱해 초기 속도 변경하는 변수
mode_selected = 0 # mode page에서 선택한 모드 저장할 변수
set_difficulty = 0 # difficulty page에서 선택한 초기 난이도
score = 0
max_score = 99999
score_2P = 0
level = 1
level_2P = 1
difficulty = 0
goal = level * 2
goal_2P = level_2P * 2
bottom_count = 0
bottom_count_2P = 0
hard_drop = False
hard_drop_2P = False
input_box = pygame.Rect(100,300,140,32)
active = True
attack_point = 0
attack_point_2P = 0
comboCounter =0
fever_score = 500
hard_score = 500
next_fever = 500
fever_interval = 3
interval = 3
comboCounter =0

# 아이템 관련 변수들
item_list = [] # 변하면 안 됨
inven = [] # 변함
dx_inven1 = int(SCREEN_WIDTH * 0.5905) # 인벤토리 1 중심의 x좌표
dx_inven2 = int(SCREEN_WIDTH * 0.6499) # 인벤토리 2 중심의 x좌표
dx_inven3 = int(SCREEN_WIDTH * 0.7093) # 인벤토리 3 중심의 x좌표
dy_inven = int(SCREEN_HEIGHT * 0.3983) # 인벤토리 y좌표(중심)
dx_inven = [dx_inven1,dx_inven2,dx_inven3] # 인벤토리 x 좌표 모음

item_size = 50 # 아이템 이미지 scale할 때 크기. 추후 출력 결과 보고 수정
# 인벤 출력할 크기로 리사이징
earthquake_inven = pygame.transform.scale(pygame.image.load("assets/images/earthquake_Item_1.png"),(item_size,item_size)) # 맨 아래줄 지우기
reset_inven = pygame.transform.scale(pygame.image.load("assets/images/reset_Item.png"),(item_size,item_size)) # 전체 블록 리셋
row_inven = pygame.transform.scale(pygame.image.load("assets/images/erase_row_Item.png"),(item_size,item_size)) # 가로 한 줄 삭제, 별도의 mino 필요
col_inven = pygame.transform.scale(pygame.image.load("assets/images/erase_col_Item.png"),(item_size,item_size)) # 세로 한 줄 삭제, 별도의 mino 필요
bomb_inven = pygame.transform.scale(pygame.image.load("assets/images/bomb_Item.png"),(item_size,item_size)) # 3x3 삭제, 별도의 mino 필요
# 별도의 블록 필요한 아이템 - block size로 리사이징
# i_row = pygame.transform.scale(pygame.image.load("assets/images/erase_row_Item.png"),(block_size,block_size)) 
# i_col = pygame.transform.scale(pygame.image.load("assets/images/erase_col_Item.png"),(block_size,block_size)) 
# i_bomb = pygame.transform.scale(pygame.image.load("assets/images/bomb_Item.png"),(block_size,block_size)) 
# 블록 그려줄 숫자 지정
#no_mino = 0 # 별도의 블록 필요없는 아이템에 부여하는 숫자
row_mino = 10  
col_mino = 11
bomb_mino = 12
#earthquake_mino = 13
#reset_mino = 14
bomb_size = 3 # bomb 아이템 썼을 때 지워줄 크기(3x3 블록 삭제이므로 3으로 설정)

item_list.append(earthquake_inven) # 아이템 리스트에 넣어줌
item_list.append(reset_inven)
item_list.append(row_inven)
item_list.append(col_inven)
item_list.append(bomb_inven)


effect_volume = 5
set_volume()

dx, dy = 3, 0  # Minos location status
dx_2P, dy_2P = 3, 0

rotation = 0  # Minos rotation status
rotation_2P = 0

mino = randint(1, 7)  # Current mino
mino_2P = randint(1, 7)

next_mino = randint(1, 7)  # Next mino
next_mino_2P = randint(1, 7)  # Next mino2

hold = False  # Hold status
hold_2P = False

hold_mino = -1  # Holded mino
hold_mino_2P = -1

player = 0
attack_stack = 0
attack_stack_2P = 0
erase_stack = 0
erase_stack_2P = 0



matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]


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
    framerate -= difficulty * speed_change


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
                    draw_reverse_board(next_mino, hold_mino, score, level, goal)
                elif pvp:
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)
                elif item: # 아이템 보드 추가
                    draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                else:
                    draw_board(next_mino, hold_mino, score, level, goal)

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
                    
                    set_difficulty = 0
                    width = DEFAULT_WIDTH
                    height = DEFAULT_HEIGHT
                    ui_variables.click_sound.play()
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
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

                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    # Game screen
    elif start:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            # 여기서 부터 겜 스타트
            elif event.type == USEREVENT:
                # Set speed
                # if not game_over:
                #     keys_pressed = pygame.key.get_pressed()
                #     if keys_pressed[K_DOWN]:
                #         pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                #     else:
                #         pygame.time.set_timer(pygame.USEREVENT, framerate * 5)
                pygame.time.set_timer(pygame.USEREVENT, framerate * 6) 
                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                
                if reverse:
                    draw_reverse_board(next_mino, hold_mino, score, level, goal)
                elif item: # 아이템 보드 추가
                    draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                else:
                    draw_board(next_mino, hold_mino, score, level, goal)
                    
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
                            draw_reverse_board(next_mino, hold_mino, score, level, goal)
                        elif item: # 아이템 보드 추가
                            draw_itemboard(next_mino, hold_mino, score, level, goal, inven)                         
                        else:
                            draw_board(next_mino, hold_mino, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
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
                for j in range(height + 1):
                    is_full = True
                    for i in range(width):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        comboCounter += 1
                        k = j
                        while k > 0:
                            for i in range(width):
                                matrix[i][k] = matrix[i][k - 1]
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
                    level += 1
                    goal += level * 2
                    framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                    # 레벨업시 이미지 출력
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))
                    pygame.display.update()
                    pygame.time.delay(200)
                    # 기존 있던 블럭들 한 칸씩 증가
                    for j in range(height):
                        for i in range(width):
                            matrix[i][j] = matrix[i][j + 1]
                    # 방해블록이 맨밑줄을 채움 # 회색블록 = 9 ,  한군데가 구멍나있게 증가
                    for i in range(width):
                        matrix[i][height] = 9
                        k = randint(1, 9)
                    matrix[k][height] = 0 # 0은 빈칸임
## 밑바닥에 비어있는 곳을 랜덤화
                # 콤보횟수에 따른 피버타임

                if values.feverTimeAddScore[1] > score >=values.feverTimeAddScore[0]:
                    ADD = values.feverAddingTime[0]
                if values.feverTimeAddScore[2] > score >= values.feverTimeAddScore[1]:
                    ADD = values.feverAddingTime[1]
                if  values.feverTimeAddScore[3] > score >= values.feverTimeAddScore[2]:
                    ADD = values.feverAddingTime[2]
                if  values.feverTimeAddScore[4] > score >= values.feverTimeAddScore[3]:
                    ADD = values.feverAddingTime[3]
                if  score >= values.feverTimeAddScore[4]:
                    ADD = values.feverAddingTime[4]     
                if comboCounter > values.feverBlockGoal:
                    if fever == False:
                        t0 = time.time()
                        fever = True
                    else:
                        t1 = time.time()
                        dt = t1 -t0                                 
                        DrawBar(barPos,barSize,borderColor,barColor, (values.Basictimer-ADD - dt)/ (values.Basictimer-ADD))                
                        mino = randint(1, 1)
                        next_mino = randint(1, 1)
                        next_fever = (c + fever_interval) * fever_score # 피버모드 점수 표시                                
                        if dt >= (values.Basictimer -ADD):
                            comboCounter =0
                            mino = next_mino
                            next_mino = randint(1, 7)                       
                            fever = False
                

                # 500~1000, 2000~2500, 3500~4000,, 단위로 장애물 등장
                if mode_selected==1:
                    for i in range(1, max_score, interval):
                        if score > i * hard_score and score < (i + 1) * hard_score: 
                            if blink1:
                                screen.blit(pygame.transform.scale(ui_variables.hard_barrier,
                                                                (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5))),
                                            [150,0])
                                blink1 = False
                            else:
                                blink1 = True
                        
                            if blink2:
                                screen.blit(pygame.transform.scale(ui_variables.hard_barrier,
                                                                (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5))),
                                            [150,250])
                                blink2 = False
                            else:
                                blink2 = True
                        
                            

                            #barrier = pygame.image.load(ui_variables.hard_barrier)
                            #barrier = pygame.transform.scale(barrier, (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5)))
                            #screen.blit(barrier, [450, 100]
                            screen.blit(pygame.transform.scale(ui_variables.hard_barrier, (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5))), [550,-50])
                
                if score == 100:            
                    get_item() # 아이템 테스트용        


                '''
                if mode_selected==1:
                    if 100<=score<200:
                        if blink1:
                            screen.blit(pygame.transform.scale(ui_variables.hard_barrier,
                                                            (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5))),
                                        [150,0])
                            blink1 = False
                        else:
                            blink1 = True
                    
                        if blink2:
                            screen.blit(pygame.transform.scale(ui_variables.hard_barrier,
                                                            (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5))),
                                        [150,250])
                            blink2 = False
                        else:
                            blink2 = True
                    '''

                        
                        
                        
                        
                    
                    

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
                    pygame.time.set_timer(pygame.USEREVENT, 2)
                    draw_mino(dx, dy, mino, rotation)
                    if reverse:
                        draw_reverse_board(next_mino, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT:
                    pygame.key.set_repeat(0)
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
                    if reverse:
                        draw_reverse_board(next_mino, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)
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
                        draw_reverse_board(next_mino, hold_mino, score, level, goal)                    
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)
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
                        draw_reverse_board(next_mino, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)

                # 왼쪽 이동, 리버스모드에선 방향키 반대
                elif event.key == K_LEFT:
                    pygame.key.set_repeat(50)
                    if reverse:
                        if not is_rightedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx += 1
                        draw_mino(dx, dy, mino, rotation)
                        draw_reverse_board(next_mino, hold_mino, score, level, goal)
                    else:
                        if not is_leftedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx -= 1
                        draw_mino(dx, dy, mino, rotation)
                        if item: # 아이템 보드 추가
                            draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                        else:
                            draw_board(next_mino, hold_mino, score, level, goal)

                # 오른쪽 이동, 리버스모드에선 방향키 반대
                elif event.key == K_RIGHT:
                    pygame.key.set_repeat(50)
                    if reverse:
                        if not is_leftedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx -= 1
                        draw_mino(dx, dy, mino, rotation)
                        draw_reverse_board(next_mino, hold_mino, score, level, goal)
                    else:
                        if not is_rightedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx += 1
                        draw_mino(dx, dy, mino, rotation)
                        if item: # 아이템 보드 추가
                            draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                        else:
                            draw_board(next_mino, hold_mino, score, level, goal)

                            

                # soft drop
                elif event.key == K_DOWN: 
                    if not is_bottom(dx, dy, mino, rotation):
                        dy +=1 
                    #pygame.time.set_timer(pygame.USEREVENT, framerate*1)
                    draw_mino(dx,dy,mino, rotation)
                    if reverse:
                        draw_reverse_board(next_mino, hold_mino, score, level, goal)
                    elif item: # 아이템 보드 추가
                        draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)
                    #pygame.display.update()

                # 아이템 사용키 1
                elif event.key == K_1:
                    key = 1
                    if item:
                        item_u = use_item(key) # 인벤의 아이템 반환
                        if item_u == row_inven:
                            mino = row_mino
                            erase_mino(dx, dy, mino, rotation)
                        elif item_u == col_inven:
                            mino = col_mino
                            erase_mino(dx, dy, mino, rotation)
                        elif item_u == bomb_inven:
                            mino = bomb_mino
                            erase_mino(dx, dy, mino, rotation)
                        elif item_u == reset_inven:
                            board_reset()
                        elif item_u == earthquake_inven:
                            earthquake()
                        
                        draw_mino(dx,dy, mino, rotation)
                        draw_itemboard(next_mino, hold_mino, score, level, goal, inven)                                       
                    
                

               
            elif event.type == KEYUP:
                pygame.key.set_repeat(300)


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
                    framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(300)
                elif erase_stack > erase_stack_2P and erase_stack >= 3:
                    erase_stack = 0
                    erase_stack_2P = 0
                    framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(300)
                elif erase_stack < erase_stack_2P and erase_stack_2P >= 3:
                    erase_stack = 0
                    erase_stack_2P = 0
                    framerate = math.ceil(framerate * FRAMERATE_MULTIFLIER_BY_DIFFCULTY[mode_selected])
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(300)


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
                    pygame.time.set_timer(pygame.USEREVENT, 2)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)

                elif event.key == K_SPACE:  # 2P#
                    ui_variables.drop_sound.play()
                    while not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, 2)
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
                    #pygame.time.set_timer(pygame.USEREVENT, framerate*1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)
                    #pygame.display.update()
                elif event.key == K_DOWN:
                    if not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        dy_2P += 1
                    #pygame.time.set_timer(pygame.USEREVENT, framerate*1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino, hold_mino, next_mino_2P, hold_mino_2P)
                    #pygame.display.update()
                    

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

                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

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
                over_start = ui_variables.h5.render("Press Enter to main page", 1, ui_variables.white)


                if reverse_over:
                    comboCounter = 0
                    draw_reverse_board(next_mino, hold_mino, score, level, goal)
                elif item: # 아이템 보드 추가
                    draw_itemboard(next_mino, hold_mino, score, level, goal, inven)
                else:
                    comboCounter = 0
                    draw_board(next_mino, hold_mino, score, level, goal)
            
            
            
                screen.blit(over_text_1, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.167))
                screen.blit(over_text_2, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.233))
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

                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if  input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                
            elif event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE: 
                    text = text[:-1]
                else:
                    text += event.unicode 
                    text_surf = font3.render(text, True, (255, 255, 255))        

                window_center = screen.get_rect().center
                screen.blit(text_surf, (input_box.x+5,input_box.y+5))
                pygame.draw.rect(screen, color, input_box, 2)
                pygame.display.flip()
                clock.tick(30)
                if event.key == K_RETURN:
                    pygame.key.set_repeat(0)
                    ui_variables.click_sound.play()                
                    ## 여기서부터 기록 저장
                    name2 = text
                    if DIFFICULTY_NAMES[current_selected] == "NORMAL": ## normal
                        istheresaved(name2,DIFFICULTY_NAMES[mode_selected])
                    if DIFFICULTY_NAMES[current_selected] == "ITEM": ## normal
                        istheresaved(name2,DIFFICULTY_NAMES[mode_selected])
                    if DIFFICULTY_NAMES[current_selected] == "HARD": ## normal
                        istheresaved(name2,DIFFICULTY_NAMES[mode_selected])
                    if DIFFICULTY_NAMES[current_selected] == "REVERSE": ## normal
                        istheresaved(name2,DIFFICULTY_NAMES[mode_selected])    
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

                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

                pygame.display.update()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

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

        START_PAGE, MENU_PAGE, HELP_PAGE, SETTING_PAGE, MODE_PAGE, DIFFICULTY_PAGE = 0, 10, 11, 12, 20, 30 # 근데 이거 숫자 의미를 모르겠음
        page, selected = START_PAGE, 0

        while not done and not start and not reverse and not pvp and not item:
            # Start Page
            if page == START_PAGE:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            pygame.key.set_repeat(0)
                            # goto menu page
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
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

                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    Rect(0, 0, int(SCREEN_WIDTH), int(SCREEN_HEIGHT * 0.24))
                )

                title = ui_variables.h1.render("TTOTRIS™", 1, ui_variables.white)
                title_menu = ui_variables.h5.render("Press space to MENU", 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Copyright (c) 2021 DOITDOIT Rights Reserved.", 1, ui_variables.grey_1)

                if blink:
                    screen.blit(title_menu, title.get_rect(center=(SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT * 0.44)))

                blink = not blink

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

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
                                page = HELP_PAGE
                            elif selected == 2:
                                # select settings menu, goto settings menu
                                ui_variables.click_sound.play()
                                page, selected = SETTING_PAGE, 0
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

                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

                block_size = int(SCREEN_HEIGHT * 0.045)
                screen.fill(ui_variables.white)
                pygame.draw.rect(
                    screen,
                    ui_variables.grey_1,
                    Rect(0, 0, int(SCREEN_WIDTH),
                         int(SCREEN_HEIGHT * 0.24))
                )

                title = ui_variables.h1.render("TTOTRIS™", 1, ui_variables.white)
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
                for event in pygame.event.get():
                    if event.type == QUIT:
                        done = True
                    elif event.type == KEYDOWN:
                        # back to menu page
                        if event.key == K_ESCAPE:
                            pygame.key.set_repeat(0)
                            ui_variables.click_sound.play()
                            page, selected = MENU_PAGE, 0
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

                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

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

                title = ui_variables.h1.render("HELP", 1, ui_variables.white)
                title_info = ui_variables.h6.render("Press esc to return menu", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                font2 = pygame.font.Font('assets/fonts/NanumGothicCoding-Bold.ttf', 15)
                title_2 = font2.render("Key help", 1, ui_variables.grey_1)
                screen.blit(title_2, title_2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 16)))

                help_text = [
                    (0, "   ", "1p      2p"),
                    (1, "조작법", "WASD    방향키"),
                    (2, "블록 홀드", "Lshift    Rshift"),
                    (3, "블록 변형", "CONTROL"),
                    (4, "하드 드롭", "E    SPACE"),
                    (5, "일시정지", "ESC")
                ]

                for h, left, right in help_text:
                    text_left = font2.render(left, 1, ui_variables.grey_1)
                    text_right = font2.render(right, 1, ui_variables.grey_1)

                    height = SCREEN_HEIGHT * (h + 6) / 16
                    left_pos = SCREEN_WIDTH * 4 / 10
                    right_pos = SCREEN_WIDTH * 6 / 10

                    screen.blit(text_left, text_left.get_rect(center=(left_pos, height)))
                    screen.blit(text_right, text_right.get_rect(center=(right_pos, height)))


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

                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

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

                title = ui_variables.h1.render("SETTINGS", 1, ui_variables.white)

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
                    "기본 테트리스 모드입니다.",
                    "게임 중 방해 요소가 포함된 모드입니다.",
                    "1P 2P 로 플레이 할 수 있는 PvP모드 입니다.",
                    "아이템 사용이 가능한 모드입니다.",
                    "방향키와 블록 등장이 반대인 리버스모드 입니다."
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

                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

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
                ## 여기에 모드별 점수를 blit
                font2 = pygame.font.Font('assets/fonts/NanumGothicCoding-Bold.ttf', 15)
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
                
                title = ui_variables.h1.render(difficulty_name, 1, ui_variables.white)
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
                            if set_difficulty >= 9: # 변수 설정 시 set_difficulty = 0으로 미리 초기화
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
                                #hard = True
                                start = True # 수빈이 수정하는 거에 따라서 변경
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
                                item = True # 구현 -> start=False 하면 될듯
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

                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        
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
                title = ui_variables.h1.render("DIFFICULTY", 1, ui_variables.white)

                title_info1 = ui_variables.h6.render("Press up and down to change speed, space to start game", 1, ui_variables.grey_1)
                title_info2 = ui_variables.h6.render("Press esc to return to mode page", 1, ui_variables.grey_1)

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))

                screen.blit(title_info1, title_info1.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200)))
                screen.blit(title_info2, title_info2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220)))
    
                
                
                velocity = ui_variables.h2.render(str(set_difficulty), 1, ui_variables.black)
                pos_velocity = velocity.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 15 ))
		            # center: 지정한 좌표가 velocity 텍스트의 중심에  가게
                screen.blit(velocity, pos_velocity)
                
                if set_difficulty > 0: # 0 이하이면 아래쪽 삼각형 안 보이게 하려는 조건
                    pos = [[SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2 + 90],
                           [SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 + 60],
                           [SCREEN_WIDTH / 2 + 30, SCREEN_HEIGHT / 2 + 60]]
                    pygame.draw.polygon(screen, ui_variables.black, pos, 0) # 원하는 좌표에 삼각형 그리기
			            # pos, 1하면 두께 1로 선만, 0 하면 채우기

                if set_difficulty < 9: # 9 이상이면 위쪽 삼각형 안 보이게 하려는 조건
                    pos = [[SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2 - 60],
                           [SCREEN_WIDTH / 2 - 30 , SCREEN_HEIGHT / 2 - 30],
                           [SCREEN_WIDTH / 2 + 30, SCREEN_HEIGHT / 2 - 30]]
		                    # 좌표 계산해서 넣기
                    pygame.draw.polygon(screen, ui_variables.black, pos, 0) 
                
                
                # 숫자가 깜빡이면 정신 없는 것 같아서 뺌. 깜빡이고 싶으면 아래 코드 넣기
                '''
                if blink: 
                    screen.blit(velocity, pos_velocity)

                blink = not blink
                '''
            if not start:
                pygame.display.update()
                clock.tick(3)
pygame.quit()