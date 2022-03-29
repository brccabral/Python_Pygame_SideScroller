import pygame
from settings import WINDOW_HEIGHT


class BG(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, scale_factor: float):
        super().__init__(groups)
        bg_image = pygame.image.load("graphics/environment/background.png").convert()
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_bg = pygame.transform.scale(bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_bg, (0, 0))
        self.image.blit(full_sized_bg, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt: float):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, scale_factor: float):
        super().__init__(groups)

        # image
        ground_image = pygame.image.load(
            "graphics/environment/ground.png"
        ).convert_alpha()
        scaled_size = pygame.Vector2(ground_image.get_size()) * scale_factor
        self.image = pygame.transform.scale(ground_image, scaled_size)

        # position
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt: float):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
