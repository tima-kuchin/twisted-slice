import pygame
from config import *
import math
import random
from threading import Timer


class Delay:
    def __init__(self, delay_time):
        self.delay_time = delay_time
        self.active = False
        self.start_time = 0

    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.delay_time:
                self.active = False

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class GUI(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GUI_LAYER
        self.groups = self.game.all_spites, self.game.GUI
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = WIN_WIDTH
        self.height = 150

        self.image = self.game.gui_img.get_sprite(0, 0, 750, 150)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class RoomMapRect(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = MAP_LAYER
        self.groups = self.game.all_spites, self.game.map
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_MAP + MAP_X
        self.y = y * TILESIZE_MAP + MAP_Y
        self.width = TILESIZE_MAP
        self.height = TILESIZE_MAP

        self.image = self.game.map_spritesheet.get_sprite(0, 0, TILESIZE_MAP, TILESIZE_MAP)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class BossMapRect(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = MAP_LAYER
        self.groups = self.game.all_spites, self.game.map
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_MAP + MAP_X
        self.y = y * TILESIZE_MAP + MAP_Y
        self.width = TILESIZE_MAP
        self.height = TILESIZE_MAP

        self.image = self.game.map_spritesheet.get_sprite(90, 0, TILESIZE_MAP, TILESIZE_MAP)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class ShopMapRect(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = MAP_LAYER
        self.groups = self.game.all_spites, self.game.map
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_MAP + MAP_X
        self.y = y * TILESIZE_MAP + MAP_Y
        self.width = TILESIZE_MAP
        self.height = TILESIZE_MAP

        self.image = self.game.map_spritesheet.get_sprite(60, 0, TILESIZE_MAP, TILESIZE_MAP)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class TreasureMapRect(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = MAP_LAYER
        self.groups = self.game.all_spites, self.game.map
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_MAP + MAP_X
        self.y = y * TILESIZE_MAP + MAP_Y
        self.width = TILESIZE_MAP
        self.height = TILESIZE_MAP

        self.image = self.game.map_spritesheet.get_sprite(30, 0, TILESIZE_MAP, TILESIZE_MAP)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Health(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GUI_LAYER
        self.groups = self.game.all_spites, self.game.health
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * 36 + HEALTH_BAR_X
        self.y = y * 36 + HEALTH_BAR_Y
        self.width = 29
        self.height = 28

        self.image = self.game.health_img.get_sprite(0, 0, 29, 28)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_spites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE - 3
        self.height = TILESIZE - 3
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1
        self.image = self.game.character_spritesheet.get_sprite(0, 0, 48, 48)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.door_blocking = True
        self.is_immortal = False
        self.time = None


    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()



        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_doors('x', self.game.level)
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_treasure_doors('y', self.game.level)
        self.collide_shop_doors('y', self.game.level)
        self.collide_doors('y', self.game.level)


        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_doors(self, direction, level):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.doors, False)
            if hits and not self.door_blocking:
                if self.x_change > 0:
                    self.game.room_now += 1
                    self.door_blocking = True
                    self.game.delay_doors.start()
                    self.game.level_change(self.game.in_treasure, self.game.in_shop)
                if self.x_change < 0:
                    self.game.room_now -= 1
                    self.door_blocking = True
                    self.game.delay_doors.start()
                    self.game.level_change(self.game.in_treasure, self.game.in_shop)
            if hits and self.door_blocking:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

    def collide_treasure_doors(self, direction, level):
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.treasure_doors, False)
            if hits and not self.door_blocking:
                if self.y_change < 0:
                    self.game.in_treasure = True
                    self.door_blocking = True
                    self.game.delay_doors.start()
                    self.game.level_change(self.game.in_treasure, self.game.in_shop)
                if self.y_change > 0:
                    self.game.in_treasure= False
                    self.door_blocking = True
                    self.game.delay_doors.start()
                    self.game.level_change(self.game.in_treasure, self.game.in_shop)
            if hits and self.door_blocking:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_shop_doors(self, direction, level):
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.shop_doors, False)
            if hits and not self.door_blocking:
                if self.y_change > 0:
                    self.game.in_shop = True
                    self.door_blocking = True
                    self.game.delay_doors.start()
                    self.game.level_change(self.game.in_treasure, self.game.in_shop)
                if self.y_change < 0:
                    self.game.in_shop = False
                    self.door_blocking = True
                    self.game.delay_doors.start()
                    self.game.level_change(self.game.in_treasure, self.game.in_shop)
            if hits and self.door_blocking:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            if self.game.character_health > 0 and not self.is_immortal:
                self.game.character_health -= 1
                self.is_immortal = True
                self.game.delay_immortality.start()
                for sprite in self.game.health:
                    sprite.kill()
                self.game.create_hp()

            if self.game.character_health == 0:
                self.kill()
                self.game.playing = False
                self.game.end = True
                self.game.character_health = CHARACTER_HEALTH

    def immortality(self):
        if self.is_immortal and not self.game.delay_immortality.active:
            self.is_immortal = False

    def block_doors(self):
        if self.door_blocking and not self.game.delay_doors.active:
            self.door_blocking = False
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(0, 0, 50, 50),
                           self.game.character_spritesheet.get_sprite(50, 0, 50, 50),
                           self.game.character_spritesheet.get_sprite(100, 0, 50, 50),
                           self.game.character_spritesheet.get_sprite(150, 0, 50, 50)]
        up_animations = [self.game.character_spritesheet.get_sprite(0, 50, 50, 50),
                         self.game.character_spritesheet.get_sprite(50, 50, 50, 50),
                         self.game.character_spritesheet.get_sprite(100, 50, 50, 50),
                         self.game.character_spritesheet.get_sprite(150, 50, 50, 50)]
        left_animations = [self.game.character_spritesheet.get_sprite(0, 150, 50, 50),
                           self.game.character_spritesheet.get_sprite(50, 150, 50, 50),
                           self.game.character_spritesheet.get_sprite(100, 150, 50, 50),
                           self.game.character_spritesheet.get_sprite(150, 150, 50, 50)]
        right_animations = [self.game.character_spritesheet.get_sprite(0, 100, 50, 50),
                            self.game.character_spritesheet.get_sprite(50, 100, 50, 50),
                            self.game.character_spritesheet.get_sprite(100, 100, 50, 50),
                            self.game.character_spritesheet.get_sprite(150, 100, 50, 50)]
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, 50, 50)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 50, 50, 50)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 150, 50, 50)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 100, 50, 50)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_spites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(50, 0, 50, 50)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = DOOR_LAYER
        self.groups = self.game.all_spites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(100, 0, 50, 50)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TreasureDoor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = DOOR_LAYER
        self.groups = self.game.all_spites, self.game.treasure_doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(150, 0, 50, 50)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class ShopDoor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = DOOR_LAYER
        self.groups = self.game.all_spites, self.game.shop_doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(200, 0, 50, 50)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Level:
    def __init__(self, rooms, is_complete=False):
        self.rooms = list(rooms)
        self.is_complete = is_complete

    def get_room(self, i):
        return self.rooms[i]

    def get_treasure(self):
        return self.rooms[-1]

    def get_shop(self):
        return self.rooms[-2]


class Room:
    def __init__(self, tilemap):
        self.tilemap = list(tilemap)
        self.is_complete = False

    def get_tilemap(self):
        return self.tilemap

    def cleaned(self):
        for i in range(len(self.tilemap)):
            self.tilemap[i] = self.tilemap[i].replace('E', '.')


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_spites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = game.terrain_spritesheet.get_sprite(0, 0, 50, 50)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_spites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, 50, 50)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):

        left_animations = [self.game.enemy_spritesheet.get_sprite(0, 50, 50, 50),
                           self.game.enemy_spritesheet.get_sprite(50, 50, 50, 50),
                           self.game.enemy_spritesheet.get_sprite(100, 50, 50, 50)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(0, 100, 50, 50),
                            self.game.enemy_spritesheet.get_sprite(50, 100, 50, 50),
                            self.game.enemy_spritesheet.get_sprite(100, 100, 50, 50)]

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0, 50, 50, 50)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0, 100, 50, 50)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Enemy_Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_spites, self.game.boss
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + ARENA_DOWN
        self.width = TILESIZE * 2
        self.height = TILESIZE * 2

        self.x_change = 0
        self.y_change = 0

        self.boss_h = 200

        self.image = self.game.boss_img.get_sprite(0, 0, 100, 100)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def shot(self):
        pass

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, font_size):
        self.font = pygame.font.Font('Minecraft.ttf', font_size)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_spites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.boss_h = 0

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()
    def collide(self):
        pygame.sprite.spritecollide(self, self.game.enemies, True)
        # self.game.kill_ghost.set_volume(self.game.sound_sfx / 100)
        # self.game.kill_ghost.play()
        pygame.sprite.spritecollide(self, self.game.boss, True)
        self.game.check_enemies()

    def animate(self):
        direction = self.game.player.facing
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 100, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(50, 100, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(100, 100, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(150, 100, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(200, 100, self.width, self.height)]
        down_animations = [self.game.attack_spritesheet.get_sprite(0, 50, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(50, 50, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(100, 50, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(150, 50, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(200, 50, self.width, self.height)]
        left_animations = [self.game.attack_spritesheet.get_sprite(0, 50, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(50, 150, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(100, 150, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(150, 150, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(200, 150, self.width, self.height)]
        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(50, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(100, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(150, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(200, 0, self.width, self.height)]
        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()