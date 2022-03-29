import random
import pygame
from settings import WINDOW_HEIGHT, WINDOW_WIDTH


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


class Plane(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, scale_factor: float):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 600
        self.direction = 0

    def import_frames(self, scale_factor: float):
        self.frames = []
        for index in range(3):
            image = pygame.image.load(f"graphics/plane/red{index}.png").convert_alpha()
            scaled_size = pygame.Vector2(image.get_size()) * scale_factor
            scaled_image = pygame.transform.scale(image, scaled_size)
            self.frames.append(scaled_image)

    def update_gravity(self, dt: float):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -400

    def animate(self, dt: float):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotation = -self.direction * 0.06
        scale = 1
        self.image = pygame.transform.rotozoom(self.image, rotation, scale)

    def update(self, dt: float):
        self.update_gravity(dt)
        self.animate(dt)
        self.rotate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, scale_factor: float):
        super().__init__(groups)

        orientation = random.choice(("up", "down"))

        image = pygame.image.load(
            f"graphics/obstacles/{random.choice((0,1))}.png"
        ).convert_alpha()
        scaled_size = pygame.Vector2(image.get_size()) * scale_factor
        self.image = pygame.transform.scale(image, scaled_size)

        x = WINDOW_WIDTH + random.randint(40, 100)

        if orientation == "down":
            y = -random.randint(10, 50)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, y))
        elif orientation == "up":
            y = WINDOW_HEIGHT + random.randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt: float):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)

        if self.rect.right <= -100:
            self.kill()
