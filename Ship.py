import random, pygame


class Ship(pygame.sprite.Sprite):

    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load("Images/boat.bmp")
        self.image.set_colorkey((0, 0, 0))
        self.x = x
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed

    def move_right(self):
        self.x += self.speed
        self.rect.x = self.x

    def move_left(self):
        self.x -= self.speed
        self.rect.x = self.x
