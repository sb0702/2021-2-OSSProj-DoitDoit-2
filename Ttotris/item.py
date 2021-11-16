import pygame
from random import *
from pygame.locals import *
from Pintris import *
from ui import *
from mino import *

item_list, inven = [],[]
item_size = block_size # 둘 다 17로 맞춰줌 출력화면 보고 사이즈 조절
double_score = pygame.transform.scale(pygame.image.load("assets/images/double_score.png"),(item_size,item_size))
item_list.append(double_score)
num_double = 10 # 만약에 블록 안에 이미지 넣어줄 거면 사용할 상수

# int(SCREEN_WIDTH * 0.2375): 사이드바의 너비
# sidebar_width = int(SCREEN_WIDTH * 0.5312): 사이드바의 x좌표

# 여기 좌표들은 이미지의 center로 넣어주기
dx_inven1 = int(SCREEN_WIDTH * 0.5905) # 인벤토리 1의 x좌표
dx_inven2 = int(SCREEN_WIDTH * 0.6499) # 인벤토리 2의 x좌표
dx_inven3 = int(SCREEN_WIDTH * 0.7093) # 인벤토리 3의 x좌표
dy_inven = int(SCREEN_HEIGHT * 0.3983) # 인벤토리 y좌표

