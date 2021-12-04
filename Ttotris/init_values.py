import pygame
import operator
import wave
import os
from mino import *
from ui import *
from random import *
from pygame.locals import *

pygame.init()

# Constants 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FRAMERATE_MULTIFLIER_BY_DIFFCULTY = [0.9, 0.8, 0.9, 0.9, 0.9] # pvp, item, reverse는 normal과 같은 비율
DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 20

# Define
block_size = 17  # Height, width of single block
width = DEFAULT_WIDTH  # Board width 가로 칸 수
height = DEFAULT_HEIGHT  # Board height 세로 칸 수
c = 0
mino_size = 4
mino_turn = 4
fever = False
color_IDactive = pygame.Color('lightskyblue3')
color_inIDactive = pygame.Color('blue')
color_Passactive = pygame.Color('lightskyblue3')
color_inPassactive = pygame.Color('blue')
IDcolor = color_inIDactive
Passcolor = color_inPassactive
barrier1=False
framerate = 30  # Bigger -> Slower
barPos      = (int(SCREEN_WIDTH*0.55), int(SCREEN_HEIGHT*0.34))
barSize     = (int(SCREEN_WIDTH * 0.2), int(SCREEN_HEIGHT*0.03))
borderColor = (0, 0, 0)
barColor    = (0, 128, 0)
min_width = 600
min_height = 350
board_rate = 0.5
input_IDactive = True

# pages
blink = False
blink1 = False
blink2 = False
blink3 = False
start = False

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
hard_erase = False
q = 0 

# Initial values
speed_change = 2.2 # 게임 시작 시 difficulty에 곱해 초기 속도 변경하는 변수
mode_selected = 0 # mode page에서 선택한 모드 저장할 변수
set_difficulty = 0 # difficulty page에서 선택한 초기 난이도
score = 0
max_score = 99999
score_2P = 0
level = 1
level_2P = 1
comboCounter =0
difficulty = 0
goal = level * 2
goal_2P = level_2P * 2
bottom_count = 0
bottom_count_2P = 0
hard_drop = False
hard_drop_2P = False
effect_volume = 5
background_music = True 

dx, dy = 3, 0  # Minos location status
dx_2P, dy_2P = 3, 0

rotation = 0  # Minos rotation status
rotation_2P = 0

mino = randint(1, 7)  # Current mino 
mino_2P = randint(1, 7)
item_mino = randint(1,9) # 아이템 모드에서 사용할 mino

next_mino1 = randint(1, 7)  # Next mino
next_mino2 = randint(1, 7) # 다다음 블록

next_mino = randint(1,7) # pvp용
next_mino_2P = randint(1, 7)  

hold = False  # Hold status
hold_2P = False

hold_mino = -1  # Holded mino
hold_mino_2P = -1

matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]

player = 0
attack_stack = 0
attack_stack_2P = 0
erase_stack = 0
erase_stack_2P = 0
attack_point = 0
attack_point_2P = 0

# 하드 모드 관련 변수들 
hard_score = 500
interval = 3
hard_i = 1
barrier_size = 1200 # 장애물 사이즈

# 피버 관련
next_fever = 500
fever_interval = 3
fever_score =500
fever = False
feverAddingTime = [0,1,2,3,4] ## 피버 조건 달성시 추가되는 time
feverTimeAddScore = [0,1500,5000,15000,30000] ## 추가적인 피버타임을 얻기 위한 점수 구간 설정
feverBlockGoal = 0 ## 몇 개의 블럭을 격파해야 피버가 주어지는지를 정하는 변수
Basictimer = 15
fever_score = 500 

# 아이템 관련
item_list = [] # 아이템 종류 담기, 게임 중 변화 x
inven = [] # 인벤토리, 변화 o 
inven_size = 50 # 인벤토리 사이즈
 # 아이템 리스트에 넣어줌
earthquake_inven = pygame.image.load("assets/images/earthquake_Item_1.png") # 맨 마지막 줄 지우기
reset_inven = pygame.image.load("assets/images/reset_Item.png") # 전체 블록 리셋
row_inven = pygame.image.load("assets/images/erase_row_Item.png") # 가로 한 줄 삭제, 별도의 mino 필요
col_inven = pygame.image.load("assets/images/erase_col_Item.png") # 세로 한 줄 삭제, 별도의 mino 필요
bomb_inven = pygame.image.load("assets/images/bomb_Item.png") # 3x3 삭제, 별도의 mino 필요

item_list.append(earthquake_inven) 
item_list.append(reset_inven)
item_list.append(row_inven)
item_list.append(col_inven)
item_list.append(bomb_inven)
 # 별도의 mino 필요한 아이템들에 부여하는 번호
row_mino = 10  
col_mino = 11
bomb_mino = 12
itembox_mino = 13  # 물음표 블록
bomb_size = 3 # bomb 아이템 썼을 때 지워줄 크기(3x3 블록 삭제이므로 3으로 설정)

# 로그인 관련
IDchoice = False
Passchoice = False
password2 = 0