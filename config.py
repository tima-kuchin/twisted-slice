import random
import math

WIN_HEIGHT = 600
WIN_WIDTH = 750
ARENA_HEIGHT = 450
ARENA_WIDTH = 750
ARENA_DOWN = WIN_HEIGHT - ARENA_HEIGHT

HEALTH_BAR_X = 530
HEALTH_BAR_Y = 45

CHARACTER_HEALTH = 1

FPS = 30
TILESIZE = 50
PLAYER_SPEED = 5
TILESIZE_MAP = 30
MAP_X = 70
MAP_Y = 38


PLAYER_LAYER = 4
BLOCK_LAYER = 2
GROUND_LAYER = 1
ENEMY_LAYER = 3
DOOR_LAYER = 2
GUI_LAYER = 10
MAP_LAYER = 11


ENEMY_SPEED = 2


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

r1_l1 = [
    'BBBBBBBBBBBBBBB',
    'B......E....BBB',
    'B......E.....BB',
    'BB....BBB....BB',
    'BBB....PBB....D',
    'BB....BBB....BB',
    'B......E.....BB',
    'B......E....BBB',
    'BBBBBBBBBBBBBBB'
]

r2_l1 = [
    'BBBBBBBTBBBBBBB',
    'B......E......B',
    'B.B.B.....B.B.B',
    'B..B.B...B.B..B',
    'D......P...E..D',
    'B..B.B...B.B..B',
    'B.B.B.....B.B.B',
    'B......E......B',
    'BBBBBBBBBBBBBBB'
]

r3_l1 = [
    'BBBBBBBBBBBBBBB',
    'B.............B',
    'B.............B',
    'B.............B',
    'D......P......D',
    'B.............B',
    'B...E.........B',
    'B..........E..B',
    'BBBBBBBSBBBBBBB'
]

treasure = [
    'BBBBBBBBBBBBBBB',
    'B.............B',
    'B.............B',
    'B.............B',
    'B.............B',
    'B.............B',
    'B.............B',
    'B......P......B',
    'BBBBBBBTBBBBBBB'
]

shop = [
    'BBBBBBBSBBBBBBB',
    'B......P......B',
    'B.............B',
    'B.............B',
    'B.............B',
    'B.............B',
    'B.............B',
    'B.............B',
    'BBBBBBBBBBBBBBB'
]

boss_l1 = [
    'BBBBBBBBBBBBBBB',
    'B.............B',
    'B..BB.....BB..B',
    'B..B.......B..B',
    'D......O......B',
    'B..B.......B..B',
    'B..BB.....BB..B',
    'B......P......B',
    'BBBBBBBBBBBBBBB'
]

rooms_l1= [r1_l1, r2_l1, r3_l1, boss_l1, shop, treasure]

map = ['.T..',
       'RRRB',
       '..S.'
]