import pygame
from pygame import font

class values:
    feverAddingTime = [0,1,2,3,4] ## 피버 조건 달성시 추가되는 time
    feverTimeAddScore = [0,1500,5000,15000,30000] ## 추가적인 피버타임을 얻기위한 점수 구간설정
    feverBlockGoal = 3 ## 몇개의 블럭을 격파해야 피버가 주어지는지를 정하는 변수
    Basictimer = 15