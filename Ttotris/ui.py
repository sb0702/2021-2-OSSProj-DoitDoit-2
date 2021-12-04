import pygame
import wave
from pygame import font
from pygame.locals import *

class ui_variables:
    pygame.init()
    # Fonts
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"
    font_path_s = "./assets/fonts/OpenSans-Semibold.ttf"
    
    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h1_s = pygame.font.Font(font_path_s, 50)

    h2_i = pygame.font.Font(font_path_i, 28)
    h5_i = pygame.font.Font(font_path_i, 13)

    # 로그인 관련
    text = ""
    loginText=""
    input_active = True
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('blue')

    # Sounds
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    background_sound = pygame.mixer.Sound("assets/sounds/SFX_Background.ogg")
    item_eraseline = pygame.mixer.Sound("assets/sounds/SFX_ItemEraseLine.wav")
    item_getuse = pygame.mixer.Sound("assets/sounds/SFX_ItemGet.wav")
    

    # image
    levelup = pygame.image.load("assets/images/levelup.png")
    fever_image = pygame.image.load("assets/images/bubble_explo4.png")
    pvp_win_image = pygame.image.load("assets/images/win.png")
    pvp_lose_image = pygame.image.load("assets/images/lose.png")
    pvp_annoying_image = pygame.image.load("assets/images/annoying.png")
    delete = pygame.transform.scale(pygame.image.load("assets/images/fever.png"),(25,25))
    hard_barrier = pygame.image.load("assets/images/ink.png")
    loginScreen = pygame.image.load("assets/images/loginscreen_transparent.png")
    

    cyan_image ='assets/images/blocks/cyan.png' 
    blue_image = 'assets/images/blocks/blue.png'
    orange_image = 'assets/images/blocks/orange.png'
    green_image = 'assets/images/blocks/green.png'
    pink_image = 'assets/images/blocks/pink.png'
    red_image = 'assets/images/blocks/red.png' 
    yellow_image = 'assets/images/blocks/yellow.png' 
    ghost_image = 'assets/images/blocks/ghost.png'
    table_image = 'assets/images/blocks/table.png' 
    addLine_image ='assets/images/blocks/addLine.png'
    bomb_image = 'assets/images/blocks/bomb_Item.png'  # bomb image
    row_image = 'assets/images/blocks/erase_row_Item.png' # erase_row image
    col_image = 'assets/images/blocks/erase_col_Item.png' # erase_col image
    itembox_image = 'assets/images/blocks/itembox.png' 

    help_key = 'assets/images/keyhelp_eng.png'
    help_item = 'assets/images/help_item.png'

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
    row_i = (11, 11, 11)  # row_item 
    col_i = (12, 12, 12)  # row_item 
    bomb_i = (13, 13, 13)  # row_item 
    i_box = (14, 14, 14) # item_box
    
    # blocks
    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3, grey_4, row_i, col_i, bomb_i, i_box] # 8: ghost, 9: 장애물

    t_block = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
                ghost_image, addLine_image, row_image, col_image, bomb_image, itembox_image] # item_image 넣기, draw_itemboard에서 사용
 
