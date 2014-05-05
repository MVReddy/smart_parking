__author__ = 'craig'
import pygame

class Player(pygame.sprite.Sprite):

    _position = (0,0) 
    
    @property
    def position(self): 
        return self._position

    @position.setter
    def position(self, position):
        self._position = position 

    def __init__(self, center, filename):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(filename).convert_alpha()
        except IOError:
            print("Cannot find player file {}".format(filename))
        self.rect = self.image.get_rect()
        self.rect.center = center
         

