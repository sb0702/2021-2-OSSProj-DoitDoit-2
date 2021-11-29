import pygame
from pygame import font

class values:
    ## 게임 세부 수치
    framerate = 30   # Bigger -> Slower
    board_rate = 0.5
    FRAMERATE_MULTIFLIER_BY_DIFFCULTY = [0.9, 0.8, 0.9, 0.9, 0.9] # pvp, item, reverse는 normal과 같은 비율
    # 피버관련 변수들
    fever = False
    feverAddingTime = [0,1,2,3,4] ## 피버 조건 달성시 추가되는 time
    feverTimeAddScore = [0,1500,5000,15000,30000] ## 추가적인 피버타임을 얻기위한 점수 구간설정
    feverBlockGoal = 3 ## 몇개의 블럭을 격파해야 피버가 주어지는지를 정하는 변수
    Basictimer = 15
    barriertimer=10
    fever_score = 500 # 수빈