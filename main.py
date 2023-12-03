from sprites import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Twisted Slice')
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font('Minecraft.ttf', 30)
        self.font_cons = pygame.font.Font('Minecraft.ttf', 20)
        self.font_header = pygame.font.Font('Minecraft.ttf', 40)
        self.font_stylized = pygame.font.Font('8BitLimitBrk.ttf', 60)

        self.running = True
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.map_spritesheet = Spritesheet('img/map.png')
        self.intro_background = pygame.image.load('./img/introbackground.png')
        self.go_background = pygame.image.load('./img/gameover.png')
        self.gui_img = Spritesheet('./img/GUI.png')
        self.boss_img = Spritesheet('./img/boss.png')
        self.health_img = Spritesheet('./img/health.png')

        self.punch_sound = pygame.mixer.Sound('sounds/punch.wav')
        self.lose_sound = pygame.mixer.Sound('sounds/lose.wav')

        self.menu_music = 'sounds/menu_music.mp3'
        self.arena_music = 'sounds/arena_music.mp3'

        self.music_mixer = pygame.mixer.music

        self.coins = 0
        self.keys = 0
        self.bombs = 0

        self.menu = True
        self.intro = True
        self.settings = False
        self.exit = False
        self.end = False
        self.playing = False
        self.is_paused = False
        self.exit_menu = False
        self.learning = False

        self.sound_sfx = 100
        self.sound_music = 100

        self.character_health = CHARACTER_HEALTH

        self.delay_immortality = Delay(2000)
        self.delay_doors = Delay(1000)

        rooms_in_level_1 = []
        rooms = list(rooms_l1)
        for room in rooms:
            rooms_in_level_1.append(Room(room))
        self.level = Level(rooms_in_level_1, False)
        self.room_now = 0

        self.in_treasure = False
        self.in_shop = False

    def reset_level(self):
        rooms_in_level_1 = []
        rooms = list(rooms_l1)
        for room in rooms:
            rooms_in_level_1.append(Room(room))
        self.level = Level(rooms_in_level_1, False)
        self.room_now = 0

    def new(self, in_treasure, in_shop):
        self.playing = True
        self.all_spites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.GUI = pygame.sprite.LayeredUpdates()
        self.health = pygame.sprite.LayeredUpdates()
        self.boss = pygame.sprite.LayeredUpdates()
        self.treasure_doors = pygame.sprite.LayeredUpdates()
        self.shop_doors = pygame.sprite.LayeredUpdates()
        self.map = pygame.sprite.LayeredUpdates()
        if in_shop:
            self.create_level(self.level.get_shop().get_tilemap())
        elif in_treasure:
            self.create_level(self.level.get_treasure().get_tilemap())
        elif not in_shop and not in_treasure:
            self.create_level(self.level.get_room(self.room_now).get_tilemap())
        self.create_map(map)
        self.create_hp()

    def create_level(self, tilemap):
        GUI(self, 0, 0)
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i)
                if column == 'D':
                    Door(self, j, i)
                if column == 'S':
                    ShopDoor(self, j, i)
                if column == 'T':
                    TreasureDoor(self, j, i)
                if column == 'O':
                    self.enemy_boss = Enemy_Boss(self, j, i)

    def create_map(self, tilemap):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == 'B':
                    BossMapRect(self, j, i)
                if column == 'R':
                    RoomMapRect(self, j, i)
                if column == 'S':
                    ShopMapRect(self, j, i)
                if column == 'T':
                    TreasureMapRect(self, j, i)

    def clean(self):
        for sprite in self.all_spites:
            sprite.kill()

    def level_change(self, in_treasure, in_shop):
        self.clean()
        self.new(in_treasure, in_shop)

    def create_hp(self):
        for row in range(max(self.character_health // 5 + 1, 1)):
            for column in range(min((self.character_health - 5 * row), 5)):
                Health(self, column, row)

    def draw_cons(self):
        keys = self.font_cons.render(str(self.keys), True, WHITE)
        keys_rect = keys.get_rect()
        keys_rect.centerx = 435
        keys_rect.centery = 33

        bombs = self.font_cons.render(str(self.bombs), True, WHITE)
        bombs_rect = bombs.get_rect()
        bombs_rect.centerx = 435
        bombs_rect.centery = 72

        coins = self.font_cons.render(str(self.coins), True, WHITE)
        coins_rect = coins.get_rect()
        coins_rect.centerx = 435
        coins_rect.centery = 112

        self.screen.blit(keys, keys_rect)
        self.screen.blit(bombs, bombs_rect)
        self.screen.blit(coins, coins_rect)
        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = True
                if event.key == pygame.K_SPACE:
                    self.play_sound_hit()
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def check_enemies(self):
        i = 0
        for sprite in self.enemies:
            i += 1
        for sprite in self.boss:
            i += 1
        if i == 0:
            self.level.get_room(self.room_now).is_complete = True
            self.level.get_room(self.room_now).cleaned()

    def play_sound_hit(self):
        self.punch_sound.set_volume(self.sound_sfx / 100)
        self.punch_sound.play()

    def update(self):
        self.all_spites.update()
        self.delay_immortality.update()
        if self.player.is_immortal:
            self.player.immortality()

        self.delay_doors.update()
        if self.player.door_blocking and self.level.get_room(self.room_now).is_complete:
            self.player.block_doors()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_spites.draw(self.screen)
        self.draw_cons()
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        self.music_mixer.load(self.arena_music)
        self.music_mixer.play(-1)
        while self.playing:
            self.events()
            self.update()
            self.draw()
            while self.is_paused:
                self.pause()
                while self.exit_menu:
                    self.exit_game_screen()

    def game_over(self):
        self.music_mixer.stop()
        self.lose_sound.play()
        text = self.font.render('Вы погибли! Начать заново?', True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 - 190))

        restart_button = Button(WIN_WIDTH/2 - 120, WIN_HEIGHT/2 - 30, 240, 50, WHITE, BLACK, 'Начать заново', 22)
        exit_to_menu_button = Button(WIN_WIDTH/2 - 120, WIN_HEIGHT/2 + 30, 240, 50, WHITE, BLACK, 'Выйти в меню', 22)

        for sprite in self.all_spites:
            sprite.kill()

        while self.end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.reset_level()
                self.end = False
                self.new(self.in_treasure, self.in_shop)
                self.main()

            if exit_to_menu_button.is_pressed(mouse_pos, mouse_pressed):
                self.menu = True
                self.intro = True
                self.end = False
                self.playing = False
                pygame.time.delay(100)

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(exit_to_menu_button.image, exit_to_menu_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        self.reset_level()
        self.music_mixer.load(self.menu_music)
        self.music_mixer.play(-1)
        title = self.font_stylized.render('Twisted Slice', True, WHITE)
        title_rect = title.get_rect()
        title_rect.centerx = WIN_WIDTH/2
        title_rect.centery = WIN_HEIGHT/2 - 120

        play_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2 - 70, 200, 50, WHITE, BLACK, 'Начать игру', 22)
        settings_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2, 200, 50, WHITE, BLACK, 'Настройки', 22)
        exit_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2 + 70, 200, 50, WHITE, BLACK, 'Выход', 22)

        while self.intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.intro = False
                    self.settings = False
                    self.menu = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro = False
                self.learning = True
                pygame.time.delay(100)

            if settings_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro = False
                self.settings = True
                pygame.time.delay(100)

            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro = False
                self.exit = True
                pygame.time.delay(100)

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(settings_button.image, settings_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def settings_screen(self):
        sound_title_sfx = self.font.render('Громкость звуков', True, WHITE)
        sound_title_sfx_rect = sound_title_sfx.get_rect()
        sound_title_sfx_rect.centerx = WIN_WIDTH / 2 - 140
        sound_title_sfx_rect.centery = WIN_HEIGHT / 2 - 75

        sound_title_music = self.font.render('Громкость музыки', True, WHITE)
        sound_title_music_rect = sound_title_music.get_rect()
        sound_title_music_rect.centerx = WIN_WIDTH / 2 - 140
        sound_title_music_rect.centery = WIN_HEIGHT / 2 + 25

        back_button = Button(WIN_WIDTH / 2 - 120, WIN_HEIGHT/2 + 80, 240, 50, WHITE, BLACK, 'Выйти в меню', 22)

        sound_sfx_plus_button = Button(WIN_WIDTH / 2 + 200, WIN_HEIGHT / 2 - 100, 50, 50, WHITE, BLACK, '+', 32)
        sound_sfx_minus_button = Button(WIN_WIDTH / 2 + 50, WIN_HEIGHT / 2 - 100, 50, 50, WHITE, BLACK, '-', 32)
        sound_music_plus_button = Button(WIN_WIDTH / 2 + 200, WIN_HEIGHT / 2, 50, 50, WHITE, BLACK, '+', 32)
        sound_music_minus_button = Button(WIN_WIDTH / 2 + 50, WIN_HEIGHT / 2, 50, 50, WHITE, BLACK, '-', 32)

        while self.settings:
            sound_title_value_sfx = self.font.render(str(self.sound_sfx), True, WHITE)
            sound_title_value_sfx_rect = sound_title_value_sfx.get_rect()
            sound_title_value_sfx_rect.centerx = WIN_WIDTH / 2 + 150
            sound_title_value_sfx_rect.centery = WIN_HEIGHT / 2 - 75

            sound_title_value_music = self.font.render(str(self.sound_music), True, WHITE)
            sound_title_value_music_rect = sound_title_value_music.get_rect()
            sound_title_value_music_rect.centerx = WIN_WIDTH / 2 + 150
            sound_title_value_music_rect.centery = WIN_HEIGHT / 2 + 25

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.intro = False
                    self.settings = False
                    self.menu = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro = True
                self.settings = False
                pygame.time.delay(100)

            if sound_sfx_plus_button.is_pressed(mouse_pos, mouse_pressed):
                if self.sound_sfx < 100:
                    self.sound_sfx += 10
                    pygame.time.delay(100)

            if sound_sfx_minus_button.is_pressed(mouse_pos, mouse_pressed):
                if self.sound_sfx > 0:
                    self.sound_sfx -= 10
                    pygame.time.delay(100)

            if sound_music_plus_button.is_pressed(mouse_pos, mouse_pressed):
                if self.sound_music < 100:
                    self.sound_music += 10
                    self.music_mixer.set_volume(self.sound_music/100)
                    pygame.time.delay(100)

            if sound_music_minus_button.is_pressed(mouse_pos, mouse_pressed):
                if self.sound_music > 0:
                    self.sound_music -= 10
                    self.music_mixer.set_volume(self.sound_music/100)
                    pygame.time.delay(100)

            self.screen.blit(self.intro_background, (0, 0))

            self.screen.blit(sound_title_sfx, sound_title_sfx_rect)
            self.screen.blit(sound_title_music,  sound_title_music_rect)

            self.screen.blit(sound_title_value_sfx, sound_title_value_sfx_rect)
            self.screen.blit(sound_title_value_music, sound_title_value_music_rect)

            self.screen.blit(back_button.image, back_button.rect)

            self.screen.blit(sound_sfx_plus_button.image, sound_sfx_plus_button.rect)
            self.screen.blit(sound_sfx_minus_button.image, sound_sfx_minus_button.rect)

            self.screen.blit(sound_music_plus_button.image, sound_music_plus_button.rect)
            self.screen.blit(sound_music_minus_button.image, sound_music_minus_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def pause(self):
        title = self.font_header.render('Пауза', True, WHITE)
        title_rect = title.get_rect()
        title_rect.centerx = WIN_WIDTH / 2
        title_rect.centery = WIN_HEIGHT / 2 - 120

        y_button = Button(WIN_WIDTH / 2 - 130, WIN_HEIGHT / 2 - 70, 260, 50, WHITE, BLACK, 'Начать с начала', 22)
        n_button = Button(WIN_WIDTH / 2 - 130, WIN_HEIGHT / 2, 260, 50, WHITE, BLACK, 'Выйти в меню', 22)

        while self.is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_paused = False
                    self.intro = False
                    self.exit = False
                    self.settings = False
                    self.menu = False
                    self.running = False
                    self.playing = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = False
                        pygame.time.delay(100)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if y_button.is_pressed(mouse_pos, mouse_pressed):
                self.reset_level()
                self.is_paused = False
                self.new(self.in_treasure, self.in_shop)
                self.main()
                pygame.time.delay(100)

            if n_button.is_pressed(mouse_pos, mouse_pressed):
                self.is_paused = False
                self.exit_menu = True
                pygame.time.delay(100)

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(y_button.image, y_button.rect)
            self.screen.blit(n_button.image, n_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def exit_game_screen(self):
        title = self.font_header.render('Вы желаете выйти в меню?', True, WHITE)
        title_rect = title.get_rect()
        title_rect.centerx = WIN_WIDTH / 2
        title_rect.centery = WIN_HEIGHT / 2 - 120

        y_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2 - 70, 200, 50, WHITE, BLACK, 'Да', 22)
        n_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2, 200, 50, WHITE, BLACK, 'Нет', 22)

        while self.exit_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.intro = False
                    self.exit = False
                    self.exit_menu = False
                    self.settings = False
                    self.menu = False
                    self.playing = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if y_button.is_pressed(mouse_pos, mouse_pressed):
                self.is_paused = False
                self.exit_menu = False
                self.end = False
                self.menu = True
                self.intro = True
                self.playing = False
                pygame.time.delay(100)

            if n_button.is_pressed(mouse_pos, mouse_pressed):
                self.is_paused = True
                self.exit_menu = False
                pygame.time.delay(100)

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(y_button.image, y_button.rect)
            self.screen.blit(n_button.image, n_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def exit_screen(self):
        title = self.font_header.render('Вы желаете выйти из игры?', True, WHITE)
        title_rect = title.get_rect()
        title_rect.centerx = WIN_WIDTH / 2
        title_rect.centery = WIN_HEIGHT / 2 - 120

        y_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2 - 70, 200, 50, WHITE, BLACK, 'Да', 22)
        n_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2, 200, 50, WHITE, BLACK, 'Нет', 22)

        while self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.intro = False
                    self.exit = False
                    self.settings = False
                    self.menu = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if y_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro = False
                self.exit = False
                self.settings = False
                self.menu = False
                self.running = False
                pygame.time.delay(100)

            if n_button.is_pressed(mouse_pos, mouse_pressed):
                self.exit = False
                self.intro = True
                pygame.time.delay(100)

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(y_button.image, y_button.rect)
            self.screen.blit(n_button.image, n_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def learning_screen(self):
        title = self.font_cons.render('Движение персожана - стрелки на клавиатуре', True, WHITE)
        title_rect = title.get_rect()
        title_rect.centerx = WIN_WIDTH / 2
        title_rect.centery = WIN_HEIGHT / 2 - 120

        title2 = self.font_cons.render('Атака - пробел', True, WHITE)
        title2_rect = title2.get_rect()
        title2_rect.centerx = WIN_WIDTH / 2
        title2_rect.centery = WIN_HEIGHT / 2 - 60

        y_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2, 200, 50, WHITE, BLACK, 'Понятно', 22)

        while self.learning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.learning = False
                    self.exit = False
                    self.exit_menu = False
                    self.settings = False
                    self.menu = False
                    self.playing = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if y_button.is_pressed(mouse_pos, mouse_pressed):
                self.music_mixer.stop()
                self.learning = False
                self.menu = False
                self.playing = True
                pygame.time.delay(100)

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(title2, title2_rect)
            self.screen.blit(y_button.image, y_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
while g.running:
    while g.menu:
        if g.intro:
            g.intro_screen()
        if g.settings:
            g.settings_screen()
        if g.exit:
            g.exit_screen()
        if g.learning:
            g.learning_screen()
    while g.playing:
        g.new(g.in_treasure, g.in_shop)
        g.main()
    while g.end:
        g.game_over()
pygame.quit()
sys.exit()
