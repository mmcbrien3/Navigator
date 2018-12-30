import random, pygame


class Obstruction(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load("Images/obstruction.bmp")
        self.image.set_colorkey((0, 0, 0))
        self.x = x
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
