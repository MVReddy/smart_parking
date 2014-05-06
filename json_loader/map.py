__author__ = 'craig'

import pygame
import random
from controller import *

class Tile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Map():
    def __init__(self, initial, initial_position):
        self.initial = initial
        self.initial_position = initial_position
        self.all_layers = initial.all_layers
        self.collision_layers = initial.collision_layers
        self.mapheight = initial.mapheight
        self.mapwidth = initial.mapwidth
        self.speed = 32

        topleft = self.all_layers[0][0].rect.topleft
        self.mapx = topleft[0]
        self.mapy = topleft[1]
        self.player = initial.player
        self.phone_width = initial.phone_rect.width
        self.phone_height = initial. phone_rect.height
        self.virtual_game_controller = GameController(initial)
        basefont = pygame.font.Font("assets/fnt/ASTONISH.TTF", 30)
        self.test_message = basefont.render("New Car", True, (0,0,0), (255, 255, 255))
        initial.test_rect = self.test_message.get_rect()



    def check_collision(self):
        adjust = [0, 0]
        if self.direction == "left":
            adjust = [self.speed, 0]
        elif self.direction == "right":
            adjust = [0- self.speed, 0]
        elif self.direction == "up":
            adjust = [0, self.speed]
        elif self.direction == "down":
            adjust = [0, 0 - self.speed]
        for collision_layer in self.collision_layers:
            tmp_list = []
            tmp_list.extend(collision_layer)
            for tile in tmp_list:
                tmp_rect = tile.rect.move(adjust)
                if tmp_rect.colliderect(self.player.rect):
                    self.clear_move = False


    def clear_to_move(self):
        self.clear_move = True

        if self.direction == "left" and self.mapx + self.speed > 0:
            self.clear_move = False
        if self.direction == "right" and self.mapx < self.phone_width - self.mapwidth - self.speed:
            self.clear_move = False
        if self.direction == "up" and self.mapy + self.speed > 0:
            self.clear_move = False
        if self.direction == "down" and self.mapy < self.phone_height - self.mapheight + self.speed:
            self.clear_move = False

        if self.clear_move and self.direction == "car_moving":
            self.check_collision()
        return (self.clear_move)


    def update(self, direction):
        x = 0
        y = 0
        self.direction = direction
        if self.clear_to_move(): 
            if direction == "right":
                x -= self.speed
            elif direction == "left":
                x += self.speed
            elif direction == "up":
                y += self.speed
            elif direction == "lup":
                x += self.speed
                y += self.speed
            elif direction == "rup":
                x -= self.speed
                y += self.speed
            elif direction == "down":
                y -= self.speed
            elif direction == "ldown":
                x += self.speed
                y -= self.speed
            elif direction == "rdown":
                x -= self.speed
                y -= self.speed
            elif direction == "start":
                x = -(self.mapx - self.initial_position[0]) 
                y = -(self.mapy - self.initial_position[1])
        else:
            print "not clear to move"
        self.move(x,y) 

    def move_to_tile(self,tile):
        tile_x = tile[0]
        tile_y = tile[1]
        x = -(self.mapx + (32*(tile_x + 1) - 546 )) - 32
        y = -(self.mapy + (32*(tile_y + 1) - 411 )) - 32
        
        self.move(x,y)
    
    def move(self, x = 0, y = 0):
        self.mapx += x
        self.mapy += y
        # Setting new position for Car Player
        self.player.position =  (-(((self.mapx - 546)/32) + 2), -(((self.mapy -411)/32) + 2))
  
        for current_layer in self.all_layers:
            for tile in current_layer:
                tile.rect.move_ip(x, y)
        for collision_layer in self.collision_layers:
            for tile in collision_layer:
                tile.rect.move_ip(x,y)

    def change_tile(self, position, layer, tile_idx): 

        for tile in self.all_layers[layer]:
            if tile.position == position:
                tile.image = self.all_layers[10][tile_idx].image 
         
    def display(self, screen):
        for layer in self.all_layers:
            for tile in layer:
                screen.blit(tile.image, tile.rect)
                 
        if self.initial.test:
            for layer in self.collision_layers:
                for collision_tile in layer:
                    screen.blit(collision_tile.image, collision_tile.rect)

            self.virtual_game_controller.gamebuttons.draw(screen)
        screen.blit(self.test_message, (5, 5))
#        if self.direction == "car_moving":  
        screen.blit(self.player.image, self.player.rect)
