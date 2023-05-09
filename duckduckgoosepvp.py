# Global Variables
import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join 
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 100
FPS2 = 60
PLAYER_VEL1 = 5
PLAYER_VEL2 = 5
yellow = (255, 255, 0)
red = (255, 0, 0)

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction = False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheets = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheets.get_width() //  width):
            surface = pygame.Surface((width,height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheets, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 64, size, size) # 96, 0, size, size
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

# def get_door(size):
#     path = join("assets", "Other", "door.png")
#     image = pygame.image.load(path).convert_alpha()
#     surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
#     rect = pygame.Rect(0, 0, size, size)
#     surface.blit(image, (0, 0), rect)
#     return pygame.transform.scale2x(surface)

# Player One
class Duck(pygame.sprite.Sprite):
    HEALTH = 100
    COLOR = (255, 0, 255)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__ (self, x, y, width, height):
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

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 2:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0 
        # self.HEALTH = self.HEALTH - self.hit_count
        # if self.HEALTH == 0:
        #     self.x_vel = 0
        #     self.y_vel = 0

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right (self,vel):
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

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    # def door(self):
    #     self.rect.x = 1000

    def update_sprite(self):
        sprite_sheet = "idlemodif"
        if self.hit:
            sprite_sheet = "hitmodif2"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet="jumpmodif"
            elif self.jump_count == 2 or self.jump_count == 3:
                sprite_sheet="double_jumpmodif"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fallmodif"

        elif self.x_vel != 0:
            sprite_sheet = "runmodif"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


# Player Two
class Goose(pygame.sprite.Sprite):
    COLOR = (255, 0, 255)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__ (self, x, y, width, height):
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

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 2:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0 

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right (self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel * 1.25, self.y_vel * 1.25)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

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
        sprite_sheet = "idlemodif"
        if self.hit:
            sprite_sheet = "hitmodif"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet="jumpmodif"
            elif self.jump_count == 2:
                sprite_sheet="double_jumpmodif"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fallmodif"

        elif self.x_vel != 0:
            sprite_sheet = "runmodif"
        
        sprite_sheet_namee = sprite_sheet + "_" + self.direction
        spritestwo = self.SPRITES[sprite_sheet_namee]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(spritestwo)
        self.spritea = spritestwo[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.spritea.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.spritea)
        
    def draw(self, win, offset_x):
        win.blit(self.spritea, (self.rect.x - offset_x, self.rect.y))


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
        self.image.blit(block, (0,0))
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
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

# class Door(Object):
#     def __init__(self, x, y, size):
#         super().__init__(x, y, size, size)
#         door = get_door(size)
#         self.image.blit(door, (0,0))
#         self.mask = pygame.mask.from_surface(self.image)

# Background
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect() # The first two underscores are x and y. We don't need them in this game
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image 

def draw(window, background, bg_image, duck, goose, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    duck.draw(window, offset_x)
    goose.draw(window, offset_x)

    pygame.display.update()

def handle_vertical_collision(duck, goose, objects, dyOne, dyTwo):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(duck, obj):
            if dyOne > 0:
                duck.rect.bottom = obj.rect.top
                duck.landed()
            elif dyOne < 0:
                duck.rect.top = obj.rect.bottom
                duck.hit_head()

            collided_objects.append(obj)

        if pygame.sprite.collide_mask(goose, obj):
            if dyTwo > 0:
                goose.rect.bottom = obj.rect.top
                goose.landed()
            elif dyTwo < 0:
                goose.rect.top = obj.rect.bottom
                goose.hit_head()
                
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


def handle_move(duck, goose, objects):
    keys = pygame.key.get_pressed()

    duck.x_vel = 0
    goose.x_vel = 0
    collide_left = collide(duck, objects, -PLAYER_VEL1 * 2)
    collide_right = collide(duck, objects, PLAYER_VEL1 * 2)
    collide_left = collide(goose, objects, -PLAYER_VEL2 * 2)
    collide_right = collide(goose, objects, PLAYER_VEL2 * 2)

    if keys[pygame.K_a] and not collide_left:
        duck.move_left(PLAYER_VEL1)
    elif keys[pygame.K_d] and not collide_right:
        duck.move_right(PLAYER_VEL1)
    if keys[pygame.K_LEFT] and not collide_left:
        goose.move_left(PLAYER_VEL2)
    elif keys[pygame.K_RIGHT] and not collide_right:
        goose.move_right(PLAYER_VEL2)


    # display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    # font = pygame.font.Font('freesansbold.ttf', 32)
    # text = font.render('GeeksForGeeks', True, red, yellow)
    # textRect = text.get_rect()

    vertical_collide = handle_vertical_collision(duck, goose, objects, duck.y_vel, goose.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            duck.make_hit()
            goose.make_hit()
        if goose.rect.x == duck.rect.x and goose.rect.y == duck.rect.y:
            duck.make_hit()

        # if obj and obj.name == "door":
        #     display_surface.blit(text, textRect)

# Main Function
def main(window):
    # Event Loop:
    clock = pygame.time.Clock()
    background, bg_image = get_background("Yellow.png")

    block_size = 96
 
    duck = Duck(200, 400, 50, 50)
    goose = Goose(300, 400, 50, 50)
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    # blocks = [Block(0, HEIGHT - block_size, block_size)]
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    # door = Door(200, HEIGHT - block_size - 64, 100)
    objects = [
        *floor, 
        Block(0, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 4, HEIGHT - block_size * 4, block_size), 
        Block(block_size * 3, HEIGHT - block_size * 7, block_size),
        Block(block_size * 4, HEIGHT - block_size * 7, block_size),
        Block(block_size * 5, HEIGHT - block_size * 7, block_size),
        Block(block_size * 3, HEIGHT - block_size * 7, block_size),
        Block(block_size * 2, HEIGHT - block_size * 7, block_size),
        Block(block_size, HEIGHT - block_size * 7, block_size),
        Block(block_size % 2, HEIGHT - block_size * 7, block_size),
        fire,
        Block(block_size * 11, HEIGHT - block_size * 7, block_size),
        Block(block_size * 12, HEIGHT - block_size * 7, block_size),
        Block(block_size * 13, HEIGHT - block_size * 7, block_size),
        Block(block_size * 14, HEIGHT - block_size * 7, block_size)
        #, door
        ]

    offset_x = 0
    offset_y = 0
    scroll_area_width = 150
    scroll_area_height = 100

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and duck.jump_count < 4:
                    duck.jump()
                if event.key == pygame.K_UP and goose.jump_count < 2:
                    goose.jump()
                
        # collideleft = collide(Duck, objects, -PLAYER_VEL1 * 2)
        # collideright = collide(Duck, objects, PLAYER_VEL1 * 2)
        # verticalcollide = handle_vertical_collision(Duck, goose, objects, Duck.y_vel, goose.y_vel)
        # to_check = [collideleft, collideright, *verticalcollide]
        # for obj in to_check:
        #     if obj and obj.name == "door":
        #         run = False
        #         break

        duck.loop(FPS2)
        goose.loop(FPS)
        fire.loop()
        handle_move(duck, goose, objects)
        draw(window, background, bg_image, duck, goose, objects, offset_x)

        keys = pygame.key.get_pressed()
        bool1 = keys[pygame.K_t]
        bool2 = keys[pygame.K_y]

        if bool1 == True:
            if (((duck.rect.right - offset_x >= WIDTH - scroll_area_width) and duck.x_vel > 0) or ((duck.rect.left - offset_x <= scroll_area_width) and duck.x_vel < 0)):
                offset_x += duck.x_vel
            if (((duck.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and duck.y_vel > 0) or ((duck.rect.top - offset_y <= scroll_area_height) and duck.y_vel < 0)):
                offset_y += (duck.y_vel * 1)

        elif bool2 == True:
            if (((goose.rect.right - offset_x >= WIDTH - scroll_area_width) and goose.x_vel > 0) or ((goose.rect.left - offset_x <= scroll_area_width) and goose.x_vel < 0)):
                offset_x += (goose.x_vel * 1.25)
            if (((goose.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and goose.y_vel > 0) or ((goose.rect.top - offset_y <= scroll_area_height) and goose.y_vel < 0)):
                offset_y += (goose.y_vel * 1)

        else:
            if (((duck.rect.right - offset_x >= WIDTH - scroll_area_width) and duck.x_vel > 0) or ((duck.rect.left - offset_x <= scroll_area_width) and duck.x_vel < 0)):
                offset_x += duck.x_vel
            if (((duck.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and duck.y_vel > 0) or ((duck.rect.top - offset_y <= scroll_area_height) and duck.y_vel < 0)):
                offset_y += (duck.y_vel * 1)
            

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)