import pygame
import operator
import math
from random import *
from pygame.locals import *
from mino import *

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

STARTING_FRAMERATE_BY_DIFFCULTY = [50, 30, 20]
FRAMELATE_MULTIFLIER_BY_DIFFCULTY = [0.9, 0.8, 0.7]

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 20

# Define
block_size = 17  # Height, width of single block
width = DEFAULT_WIDTH  # Board width
height = DEFAULT_HEIGHT  # Board height

mino_size = 4
mino_turn = 4

framerate = 30  # Bigger -> Slower

min_width = 700
min_height = 350
board_rate = 0.5

pygame.init()
pygame.key.set_repeat(500)


class ui_variables:
    # Fonts
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")

    # image
    levelup = pygame.image.load("assets/images/levelup.png")
    fever_image = pygame.image.load("assets/images/fever.png")
    pvp_win_image = pygame.image.load("assets/images/win.png")
    pvp_lose_image = pygame.image.load("assets/images/lose.png")
    pvp_annoying_image = pygame.image.load("assets/images/annoying.png")

    # Background colors
    black = (10, 10, 10)  # rgb(10, 10, 10)
    white = (255, 255, 255)  # rgb(255, 255, 255)
    grey_1 = (26, 26, 26)  # rgb(26, 26, 26)
    grey_2 = (35, 35, 35)  # rgb(35, 35, 35)
    grey_3 = (55, 55, 55)  # rgb(55, 55, 55)
    grey_4 = (100, 100, 100)
    # Tetrimino colors
    cyan = (69, 206, 204)  # rgb(69, 206, 204) # I
    blue = (64, 111, 249)  # rgb(64, 111, 249) # J
    orange = (253, 189, 53)  # rgb(253, 189, 53) # L
    yellow = (246, 227, 90)  # rgb(246, 227, 90) # O
    green = (98, 190, 68)  # rgb(98, 190, 68) # S
    pink = (242, 64, 235)  # rgb(242, 64, 235) # T
    red = (225, 13, 27)  # rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3, grey_4]


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
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )


# Draw game screen
def draw_board(next, hold, score, level, goal):
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
            dx = int(SCREEN_WIDTH * 0.025) + sidebar_width + block_size * j
            dy = int(SCREEN_HEIGHT * 0.3743) + block_size * i
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
    text_fever = ui_variables.h5.render("NEXT FEVER", 1, ui_variables.black)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.2780)))
    screen.blit(text_score, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.5187)))
    screen.blit(score_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.5614)))
    screen.blit(text_level, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.6791)))
    screen.blit(level_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.7219)))
    screen.blit(text_goal, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.8395)))
    screen.blit(goal_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.8823)))
    screen.blit(text_fever, (int(SCREEN_WIDTH * 0.12) + sidebar_width, int(SCREEN_HEIGHT * 0.8395)))
    screen.blit(next_fever_value, (int(SCREEN_WIDTH * 0.13) + sidebar_width, int(SCREEN_HEIGHT * 0.8823)))

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
            dx = int(SCREEN_WIDTH * 0.025) + sidebar_width + block_size * j
            dy = int(SCREEN_HEIGHT * 0.3743) + block_size * i
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
    text_fever = ui_variables.h5.render("NEXT FEVER", 1, ui_variables.black)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.0374)))
    screen.blit(text_next, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.2780)))
    screen.blit(text_score, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.5187)))
    screen.blit(score_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.5614)))
    screen.blit(text_level, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.6791)))
    screen.blit(level_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.7219)))
    screen.blit(text_goal, (int(SCREEN_WIDTH * 0.045) + sidebar_width, int(SCREEN_HEIGHT * 0.8395)))
    screen.blit(goal_value, (int(SCREEN_WIDTH * 0.055) + sidebar_width, int(SCREEN_HEIGHT * 0.8823)))
    screen.blit(text_fever, (int(SCREEN_WIDTH * 0.12) + sidebar_width, int(SCREEN_HEIGHT * 0.8395)))
    screen.blit(next_fever_value, (int(SCREEN_WIDTH * 0.13) + sidebar_width, int(SCREEN_HEIGHT * 0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(SCREEN_WIDTH * 0.25) + block_size * x
            dy = int(SCREEN_HEIGHT * 0.055) + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][(height - 1) - y + 1]])


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


# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]  # grid에 mino_map의 모양과 방향을 선택한 리스트를 넣는다.
    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    # Draw mino
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]


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
                matrix[i][j] = 0

    # Erase mino
    for i in range(mino_size):
        for j in range(mino_turn):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0


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


# Start game
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PINTRIS™")

# pages
blink = False
start = False
pause = False
done = False
game_over = False
reverse = False
pvp = False
reverse_over = False
pvp_over = False

# Initial values
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

attack_point = 0
attack_point_2P = 0

fever_score = 500
next_fever = 500
fever_interval = 3

# 난이도
easy_difficulty = 0
normal_difficulty = 1
hard_difficulty = 2

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

name_location = 0
name = [65, 65, 65]

with open('leaderboard.txt') as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
for i in lines:
    leaders[i.split(' ')[0]] = int(i.split(' ')[1])
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]


# 초기화 부분을 하나로 합쳐준다.
def init_game(board_width, board_height, game_difficulty):
    global width, height, matrix, matrix_2P, difficulty, framerate

    width = board_width
    height = board_height

    matrix = [[0 for y in range(board_height + 1)] for x in range(board_width)]
    matrix_2P = [[0 for y in range(board_height + 1)] for x in range(board_width)]

    difficulty = game_difficulty
    framerate = STARTING_FRAMERATE_BY_DIFFCULTY[difficulty]


###########################################################
# Loop Start
###########################################################

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
                    next_fever = 500
                    max_score = 99999
                    fever_interval = 3
                    score = 0
                    fever = 0
                    level = 1
                    goal = level * 2
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    easy_difficulty = 0
                    normal_difficulty = 1
                    hard_difficulty = 2

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
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                if reverse:
                    draw_reverse_board(next_mino, hold_mino, score, level, goal)
                else:
                    draw_board(next_mino, hold_mino, score, level, goal)
                pygame.display.update()

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level

                        draw_mino(dx, dy, mino, rotation)
                        if reverse:
                            draw_reverse_board(next_mino, hold_mino, score, level, goal)
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
                        k = j
                        while k > 0:
                            for i in range(width):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
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
                    framerate = math.ceil(framerate * FRAMELATE_MULTIFLIER_BY_DIFFCULTY[difficulty])
                    # 레벨업시 이미지 출력
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))
                    pygame.display.update()
                    pygame.time.delay(200)
                    # 기존있던블럭들 한칸증가
                    for j in range(height):
                        for i in range(width):
                            matrix[i][j] = matrix[i][j + 1]
                    # 방해블록이 맨밑줄을 채움 # 회색블록 = 9 ,  한군데가 구멍나있게 증가
                    for i in range(width):
                        matrix[i][height] = 9
                    k = randint(1, 9)
                    matrix[k][height] = 0

                # 점수 구간에 따른 피버타임 #fever_interval=3
                for i in range(1, max_score, fever_interval):
                    if score > i * fever_score and score < (i + 1) * fever_score:  # 500~1000,2000~2500.3500~4000
                        mino = randint(1, 1)
                        next_mino = randint(1, 1)
                        next_fever = (i + fever_interval) * fever_score
                        # fever time시 이미지 깜빡거리게
                        if blink:
                            screen.blit(pygame.transform.scale(ui_variables.fever_image,
                                                               (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                        (SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.1))
                            blink = False
                        else:
                            blink = True

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
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
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
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
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
                    else:
                        draw_board(next_mino, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
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
                        draw_board(next_mino, hold_mino, score, level, goal)

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


    elif pvp:
        pygame.key.set_repeat(0)  # 키반복 비활성화
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not pvp_over:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

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
                        if matrix[i][j] == 0 or matrix[i][j] == 9:
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

                # 상대방 시야 방해
                # fever_score, fever_interval 값을 이용하여 나타냄
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
                    framerate = math.ceil(framerate * FRAMELATE_MULTIFLIER_BY_DIFFCULTY[difficulty])
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(300)
                elif erase_stack > erase_stack_2P and erase_stack >= 3:
                    erase_stack = 0
                    erase_stack_2P = 0
                    framerate = math.ceil(framerate * FRAMELATE_MULTIFLIER_BY_DIFFCULTY[difficulty])
                    screen.blit(pygame.transform.scale(ui_variables.levelup,
                                                       (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2))),
                                (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.2)))  # 레벨업시 이미지 출력
                    pygame.display.update()
                    pygame.time.delay(300)
                elif erase_stack < erase_stack_2P and erase_stack_2P >= 3:
                    erase_stack = 0
                    erase_stack_2P = 0
                    framerate = math.ceil(framerate * FRAMELATE_MULTIFLIER_BY_DIFFCULTY[difficulty])
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
                    draw_reverse_board(next_mino, hold_mino, score, level, goal)
                else:
                    draw_board(next_mino, hold_mino, score, level, goal)

                screen.blit(over_text_1, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.167))
                screen.blit(over_text_2, (SCREEN_WIDTH * 0.0775, SCREEN_HEIGHT * 0.233))

                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.white)

                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.white)

                screen.blit(name_1, (SCREEN_WIDTH * 0.08125, SCREEN_HEIGHT * 0.326))
                screen.blit(name_2, (SCREEN_WIDTH * 0.11875, SCREEN_HEIGHT * 0.326))
                screen.blit(name_3, (SCREEN_WIDTH * 0.15625, SCREEN_HEIGHT * 0.326))

                if blink:
                    screen.blit(over_start, (SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.4333))
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, (SCREEN_WIDTH * 0.08125 - 2, SCREEN_HEIGHT * 0.326 - 2))
                    elif name_location == 1:
                        screen.blit(underbar_2, (SCREEN_WIDTH * 0.11875 - 2, SCREEN_HEIGHT * 0.326 - 2))
                    elif name_location == 2:
                        screen.blit(underbar_3, (SCREEN_WIDTH * 0.15625, SCREEN_HEIGHT * 0.326 - 2))
                    blink = True
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
                    pygame.key.set_repeat(0)
                    ui_variables.click_sound.play()

                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    width = DEFAULT_WIDTH  # Board width
                    height = DEFAULT_HEIGHT
                    game_over = False
                    reverse_over = False
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

                    easy_difficulty = 0
                    normal_difficulty = 1
                    hard_difficulty = 2

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

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                elif event.key == K_RIGHT:
                    pygame.key.set_repeat(0)
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    pygame.key.set_repeat(0)
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    pygame.key.set_repeat(0)
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    pygame.key.set_repeat(0)
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)

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

                    easy_difficulty = 0
                    normal_difficulty = 1
                    hard_difficulty = 2

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
        # Start page <-> Menu Page <-> Diffculty Page -> Start
        #                          <-> HelpPage
        #                          <-> SettingPage
        #
        # page는 지금 있는 page의 고유 넘버를 나타내고, 아래와 같이 상수를 사용해 가독성을 높였습니다.
        # selected는 선택지가 있는 페이지에서 몇번째  보기를 선택하고 있는지 나타내는 변수입니다.
        # 편의상 0부터 시작합니다.

        START_PAGE, MENU_PAGE, HELP_PAGE, SETTING_PAGE, DIFFICULTY_PAGE = 0, 10, 11, 12, 20
        page, selected = START_PAGE, 0

        while not done and not start and not reverse and not pvp:
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

                title = ui_variables.h1.render("PINTRIS™", 1, ui_variables.white)
                title_menu = ui_variables.h5.render("Press space to MENU", 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Copyright (c) 2021 PINT Rights Reserved.", 1, ui_variables.grey_1)

                leader_1 = ui_variables.h5_i.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1,
                                                    ui_variables.white)
                leader_2 = ui_variables.h5_i.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1,
                                                    ui_variables.white)
                leader_3 = ui_variables.h5_i.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1,
                                                    ui_variables.white)

                if blink:
                    screen.blit(title_menu, title.get_rect(center=(SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT * 0.44)))

                blink = not blink

                screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.1)))
                screen.blit(title_info, title_info.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.77)))

                screen.blit(leader_1, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT * 0.0347)))
                screen.blit(leader_2, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT * 0.0614)))
                screen.blit(leader_3, (int(SCREEN_WIDTH * 0.033), int(SCREEN_HEIGHT * 0.096)))

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
                            if selected == 0 or selected == 1:
                                # next menu select
                                ui_variables.click_sound.play()
                                selected = selected + 1
                        elif event.key == K_UP:
                            pygame.key.set_repeat(0)
                            if selected == 1 or selected == 2:
                                # previous menu select
                                ui_variables.click_sound.play()
                                selected = selected - 1
                        elif event.key == K_SPACE:
                            pygame.key.set_repeat(0)
                            if selected == 0:
                                # select start menu, goto difficulty select page
                                ui_variables.click_sound.play()
                                page, selected = DIFFICULTY_PAGE, 0
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

                title = ui_variables.h1.render("PINTRIS™", 1, ui_variables.white)
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

            # difficulty page
            elif page == DIFFICULTY_PAGE:
                # 난이도를 설정한다.
                DIFFICULTY_COUNT = 6
                DIFFICULTY_NAMES = ["EASY", "NORMAL", "HARD", "PvP", "SPEED & MINI", "REVERSE"]
                DIFFICULTY_EXPLAINES = [
                    "블록이 천천히 내려오는 이지모드 입니다.",
                    "블록이 중간 속도로 내려오는 노말모드 입니다.",
                    "블록이 빠르게 내려오는 하드모드 입니다.",
                    "1P 2P 로 플레이 할 수 있는 PvP모드 입니다.",
                    "보드 크기가 줄어든 스피드&미니모드 입니다.",
                    "방향키와 블록 등장이 반대인 리버스모드 입니다."
                ]

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
                        if event.key == K_SPACE:
                            pygame.key.set_repeat(0)
                            if 0 <= selected < 3:
                                # start game with selected difficulty
                                ui_variables.click_sound.play()
                                start = True
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, selected)

                                # PvP mode page
                            if selected == 3:
                                ui_variables.click_sound.play()
                                pvp = True
                                start = False
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, normal_difficulty)

                            if selected == 4:
                                # start game with small size
                                ui_variables.click_sound.play()
                                start = True
                                init_game(DEFAULT_WIDTH, int(DEFAULT_HEIGHT / 2), hard_difficulty)

                                # Reverse mode page
                            if selected == 5:
                                ui_variables.click_sound.play()
                                start = True
                                reverse = True
                                init_game(DEFAULT_WIDTH, DEFAULT_HEIGHT, normal_difficulty)


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
                font2 = pygame.font.Font('assets/fonts/NanumGothicCoding-Bold.ttf', 15)
                difficulty_name = DIFFICULTY_NAMES[current_selected]
                difficulty_explain = DIFFICULTY_EXPLAINES[current_selected]

                title = ui_variables.h1.render(difficulty_name, 1, ui_variables.white)
                title_explain = font2.render(difficulty_explain, 1, ui_variables.grey_1)
                title_info = ui_variables.h6.render("Press left and right to change, space to start", 1,
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

            if not start:
                pygame.display.update()
                clock.tick(3)
pygame.quit()