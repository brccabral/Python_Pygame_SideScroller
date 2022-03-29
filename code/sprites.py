import pygame


class BG(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/environment/background.png").convert()
        self.rect = self.image.get_rect(topleft=(0, 0))
