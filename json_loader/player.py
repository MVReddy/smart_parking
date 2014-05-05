__author__ = 'craig'
import pygame

class Player(pygame.sprite.Sprite):

    _initial_center = (0,0)
    
    def __init__(self, center, filename):
        pygame.sprite.Sprite.__init__(self)
        self._initial_center = (center[0], center[1])
        try:
            self.image = pygame.image.load(filename).convert_alpha()
        except IOError:
            print("Cannot find player file {}".format(filename))
        self.rect = self.image.get_rect()
        self.rect.center = center
         

