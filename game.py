import pygame
import button
from os import listdir
from os.path import isfile, join
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Riomo")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))
HEART = pygame.image.load('heart.png')


def play_main_music():
    main_music_path = join("assets", "Audio", "cottagecore-17463.mp3")
    main_music = pygame.mixer.Sound(main_music_path)
    pygame.mixer.Sound.play(main_music)

def play_jump_music():
    jump_music_path = join("assets", "Audio", "cartoon-jump-6462.mp3")
    pygame.mixer.music.load(jump_music_path)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()

def play_damage_music():
    damage_music_path = join("assets", "Audio", "2G7CF5V-gamers-fail-game.mp3")
    pygame.mixer.music.load(damage_music_path)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()

play_main_music()

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites



class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1

character_options = OptionBox(
    600, 265, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30), 
    ["MaskDude", "NinjaFrog", "PinkMan", "VirtualGuy"])

block_options = OptionBox(
    600, 460, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30), 
    ["1", "2", "3", "4", "5", "6"])

user_character = "MaskDude"
block_choice = 2



def setting(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    back_img_path = join("assets", "Menu", "Buttons", "Back.png")
    back_img = pygame.image.load(back_img_path).convert_alpha()
    back_button = button.Button(925, 20, back_img, 3.5)

    global user_character
    global block_choice

    run_setting = True

    while run_setting:
        clock.tick(FPS)

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run_setting = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_setting = False
                    menu(window)

        selected_character_option = character_options.update(event_list)
        if selected_character_option >= 0:
            if selected_character_option == 0:
                user_character = "MaskDude"
            elif selected_character_option == 1:
                user_character = "NinjaFrog"
            elif selected_character_option == 2:
                user_character = "PinkMan"
            elif selected_character_option == 3:
                user_character = "VirtualGuy"

        selected_block_option = block_options.update(event_list)
        if selected_block_option >= 0:
            if selected_block_option == 0:
                block_choice = 1
            elif selected_block_option == 1:
                block_choice = 2
            elif selected_block_option == 2:
                block_choice = 3
            elif selected_block_option == 3:
                block_choice = 4
            elif selected_block_option == 4:
                block_choice = 5
            elif selected_block_option == 5:
                block_choice = 6

        draw_setting(window, background, bg_image, back_button)

        
        pygame.display.update()

    pygame.quit()
    quit()

def get_block(size):
    if block_choice == 1:
        block_x, block_y = 0, 0
    elif block_choice == 2:
        block_x, block_y = 96, 0
    elif block_choice == 3:
        block_x, block_y = 0, 64
    elif block_choice == 4:
        block_x, block_y = 96, 64
    elif block_choice == 5:
        block_x, block_y = 0, 128
    elif block_choice == 6:
        block_x, block_y = 96, 128
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(block_x, block_y, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", user_character, 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.hearts = 3

    def jump(self):
        play_jump_music()
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True        

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0
            self.hearts -= 1
            play_damage_music()

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        Player.SPRITES = load_sprite_sheets("MainCharacters", user_character, 32, 32, True)

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, HEART_1, HEART_2, HEART_3):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
        if self.hearts == 3:
            win.blit(HEART_1, (WIDTH // 2 + 100, 50))
            
        if self.hearts >= 2:
            win.blit(HEART_2, (WIDTH // 2 , 50))

        if self.hearts >= 1:
            win.blit(HEART_3, (WIDTH // 2 - 100, 50))

        if self.hearts <= 0:
            run = False
            menu(window)
            self.hearts = 3


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Checkpoint(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "flag")
        self.flag = load_sprite_sheets("Items", "Checkpoints/checkpoint", width, height)
        self.image = self.flag["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"

    def loop(self):
        sprites = self.flag[self.animation_name]
        sprite_index = 0
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
        

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw_setting(window, background, bg_image, back_button):
    for tile in background:
        window.blit(bg_image, tile)

    font = pygame.font.Font('Caprasimo-Regular.ttf', 40)
    text = font.render('Character', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 3, HEIGHT // 2.8)
    window.blit(text, textRect)
    text_2 = font.render('Block', True, (0, 0, 0))
    textRect_2 = text_2.get_rect()
    textRect_2.center = (WIDTH // 3, 475)
    window.blit(text_2, textRect_2)

    if back_button.draw(window):
            run_setting = False
            menu(window)

    character_options.draw(window)
    block_options.draw(window)

    pygame.display.update()

def draw_menu(window, background, bg_image, start_button, setting_button, exit_button):
    red = (255, 0, 0)
    for tile in background:
        window.blit(bg_image, tile)

    if start_button.draw(window):
            run_menu = False
            main(window)

    if setting_button.draw(window):
            run_menu = False
            setting(window)
        
    if exit_button.draw(window):
            pygame.quit()
            quit()

    font = pygame.font.Font('Caprasimo-Regular.ttf', 70)
    text = font.render('RIOMO', True, red)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2.8)
    window.blit(text, textRect)

    pygame.display.update()

def draw(window, background, bg_image, player, objects, offset_x):
    HEART_1 = pygame.transform.scale(HEART, (50, 50))
    HEART_2 = pygame.transform.scale(HEART, (50, 50))
    HEART_3 = pygame.transform.scale(HEART, (50, 50))

    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x, HEART_1, HEART_2, HEART_3)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

        if obj and obj.name == "flag":
            run = False
            menu(window)


def menu(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    setting_img_path = join("assets", "Menu", "Buttons", "Settings.png")
    start_img = pygame.image.load('start_btn.png').convert_alpha()
    exit_img = pygame.image.load('exit_btn.png').convert_alpha()
    setting_img = pygame.image.load(setting_img_path).convert_alpha()

    start_button = button.Button(300, 400, start_img, 0.5)
    exit_button = button.Button(600, 400, exit_img, 0.5)
    setting_button = button.Button(925, 20, setting_img, 2.5)

    run_menu = True

    while run_menu:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    run_menu = False
                    main(window)

        draw_menu(window, background, bg_image, start_button, setting_button, exit_button)


        pygame.display.update()

    pygame.quit()
    quit()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    player = Player(block_size, HEIGHT - block_size, 50, 50)

    fire = [Fire(block_size * 3, HEIGHT - block_size - 64, 16, 32),
            Fire(block_size * 6 + 70, HEIGHT - block_size * 4 - 64, 16, 32),
            Fire(block_size * 13, HEIGHT - block_size - 64, 16, 32),
            Fire(block_size * 16, HEIGHT - block_size - 64, 16, 32)]

    checkpoint = [Checkpoint(block_size * 19, HEIGHT - block_size * 2 - 32, 50, 64)]

    blocks = [Block(0, HEIGHT - block_size * 2, block_size),
            Block(0, HEIGHT - block_size * 3, block_size),
            Block(0, HEIGHT - block_size * 4, block_size),
            Block(0, HEIGHT - block_size * 5, block_size),
            Block(0, HEIGHT - block_size * 6, block_size),
            Block(block_size * 4, HEIGHT - block_size * 3, block_size),
            Block(block_size * 4, HEIGHT - block_size * 2, block_size),
            Block(block_size * 6, HEIGHT - block_size * 4, block_size),
            Block(block_size * 7, HEIGHT - block_size * 4, block_size),
            Block(block_size * 7, HEIGHT - block_size * 4, block_size),
            Block(block_size * 10, HEIGHT - block_size * 2, block_size),
            Block(block_size * 10, HEIGHT - block_size * 3, block_size),
            Block(block_size * 10, HEIGHT - block_size * 4, block_size),
            Block(block_size * 10, HEIGHT - block_size * 5, block_size),
            Block(block_size * 13, HEIGHT - block_size * 4, block_size),
            Block(block_size * 13, HEIGHT - block_size * 5, block_size),
            Block(block_size * 13, HEIGHT - block_size * 6, block_size),
            Block(block_size * 13, HEIGHT - block_size * 7, block_size),
            Block(block_size * 13, HEIGHT - block_size * 8, block_size)]

    for i in range(len(fire)):
        fire[i].on()


    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(0, (WIDTH * 3) // block_size)]

    objects = [*floor,
                *blocks,
                *fire,
                *checkpoint]

    offset_x = 0
    scroll_area_width = 200

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

                if event.key == pygame.K_ESCAPE :
                    run = False
                    menu(window)


        player.loop(FPS)
        for i in range(len(fire)):
            fire[i].loop()
        for i in range(len(checkpoint)):
            checkpoint[i].loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()

if __name__ == "__main__":
    menu(window)